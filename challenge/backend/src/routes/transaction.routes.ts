import { Router, Response } from 'express';
import { getDb } from '../models/database';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import {
    decryptPrivateKey,
    signMessage,
    signMessageWithRS,
    verifySignature,
    createWithdrawMessage,
    createDepositReceiptMessage
} from '../services/crypto.service';


async function verifyWalletIntegrity(userId: number, requestAmount: number): Promise<boolean> {
    const db = getDb();
    const result = await db.get(
        'SELECT SUM(CASE WHEN type = "deposit" THEN amount ELSE -amount END) as calculated_balance FROM transactions WHERE user_id = ? AND status = "approved"',
        userId
    ) as any;
    
    const calculatedBalance = result?.calculated_balance || 0;
    return calculatedBalance >= requestAmount;
}

const router = Router();

router.get('/balance', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const db = getDb();
        const user = await db.get('SELECT game_balance, main_balance FROM users WHERE id = ?', userId) as any;

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({
            gameBalance: user.game_balance,
            mainBalance: user.main_balance
        });
    } catch (error) {
        console.error('Keys error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.post('/faucet', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const FAUCET_AMOUNT = 50;
        const db = getDb();

        const todayClaim = await db.get(`
            SELECT * FROM faucet_claims 
            WHERE user_id = ? AND claimed_at = date('now')
        `, userId);

        if (todayClaim) {
            return res.status(400).json({
                error: 'Already claimed today. Try again tomorrow.',
                nextClaimAt: 'tomorrow'
            });
        }

        const user = await db.get('SELECT wallet_key, private_key_encrypted, game_balance FROM users WHERE id = ?', userId) as any;

        if (!user || !user.wallet_key || !user.private_key_encrypted) {
            return res.status(400).json({ error: 'Wallet not configured' });
        }

        const privateKey = decryptPrivateKey(user.private_key_encrypted, user.wallet_key);
        const timestamp = Date.now();
        const kSeed = Math.floor(timestamp / 100);
        const nonce = Math.random().toString(36).substring(2, 10);

        const receiptMessage = createDepositReceiptMessage(userId, FAUCET_AMOUNT, timestamp, nonce);
        const receiptSignature = signMessageWithRS(privateKey, receiptMessage, kSeed);

        await db.run('UPDATE users SET game_balance = game_balance + ? WHERE id = ?', FAUCET_AMOUNT, userId);
        await db.run(`
            INSERT INTO faucet_claims (user_id, amount, sig_r, sig_s, msg_hash) 
            VALUES (?, ?, ?, ?, ?)
        `, userId, FAUCET_AMOUNT, receiptSignature.r, receiptSignature.s, receiptSignature.msgHash);

        await db.run('INSERT INTO transactions (user_id, type, amount, sig_r, sig_s, msg_hash, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
            userId, 'deposit', FAUCET_AMOUNT, receiptSignature.r, receiptSignature.s, receiptSignature.msgHash, 'approved');

        const updatedUser = await db.get('SELECT game_balance, main_balance FROM users WHERE id = ?', userId) as any;

        res.json({
            message: `Received ${FAUCET_AMOUNT} USD to Game Balance!`,
            amount: FAUCET_AMOUNT,
            gameBalance: updatedUser.game_balance,
            mainBalance: updatedUser.main_balance,
            receipt: {
                message: receiptMessage,
                msgHash: receiptSignature.msgHash,
                signature: {
                    r: receiptSignature.r,
                    s: receiptSignature.s
                },
                timestamp
            }
        });
    } catch (error) {
        console.error('Faucet error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.get('/faucet/status', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const db = getDb();
        const todayClaim = await db.get(`
            SELECT * FROM faucet_claims 
            WHERE user_id = ? AND claimed_at = date('now')
        `, userId) as any;

        const allClaims = await db.all(`
            SELECT id, amount, sig_r, sig_s, msg_hash, claimed_at, created_at
            FROM faucet_claims WHERE user_id = ?
            ORDER BY created_at DESC LIMIT 50
        `, userId);

        res.json({
            canClaim: !todayClaim,
            todayClaim: todayClaim || null,
            claims: allClaims
        });
    } catch (error) {
        console.error('Faucet status error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.get('/flag', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const db = getDb();
        const user = await db.get('SELECT game_balance, main_balance FROM users WHERE id = ?', userId) as any;

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        const FLAG_THRESHOLD = 1000000000;

        if (user.main_balance >= FLAG_THRESHOLD) {
            res.json({
                success: true,
                message: 'Here is your flag!',
                flag: process.env.FLAG || 'DH{test_flag}',
                mainBalance: user.main_balance
            });
        } else {
            res.json({
                success: false,
                message: `Need more USD in Main Balance. Use Withdraw to transfer from Game Balance.`,
                gameBalance: user.game_balance,
                mainBalance: user.main_balance,
                requiredBalance: FLAG_THRESHOLD
            });
        }
    } catch (error) {
        console.error('Flag error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.post('/withdraw', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const { amount, signature, timestamp } = req.body;
        const userId = req.userId!;

        if (!amount || amount <= 0) {
            return res.status(400).json({ error: 'Please enter a valid amount' });
        }

        const db = getDb();
        const user = await db.get('SELECT game_balance, main_balance, public_key, private_key_encrypted, wallet_key FROM users WHERE id = ?', userId) as any;

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        if (!user.public_key) {
            return res.status(400).json({ error: 'Wallet not configured' });
        }

        if (user.game_balance >= 50000 || user.main_balance >= 50000) {
             return res.status(400).json({ 
                 error: 'High value withdrawal requires manual processing. Contact administrator.',
                 code: 'MANUAL_REVIEW_REQUIRED'
             });
        }

        const now = Date.now();
        if (!timestamp || Math.abs(now - timestamp) > 5 * 60 * 1000) {
            return res.status(400).json({ error: 'Request expired or invalid timestamp' });
        }

        const message = createWithdrawMessage(userId, Number(amount), timestamp);

        let signatureToVerify = signature;

        if (!signature) {
             try {
                const privateKey = decryptPrivateKey(user.private_key_encrypted, user.wallet_key);
                signatureToVerify = signMessage(privateKey, message);
            } catch (err) {
                return res.status(500).json({ error: 'Failed to generate signature' });
            }
        }

        const isValid = verifySignature(user.public_key, message, signatureToVerify);
        if (!isValid) {
            return res.status(403).json({ error: 'Signature verification failed' });
        }
        
        let isServerSigned = !signature; 

        if (isServerSigned) {
            const isIntegrityVerified = await verifyWalletIntegrity(userId, amount);
            if (!isIntegrityVerified) {
                 return res.status(400).json({ error: 'Integrity check failed: Potential replay or consistency error' });
            }
        }
        
        const newGameBalance = user.game_balance - amount;
        const newMainBalance = user.main_balance + amount;

        await db.run('UPDATE users SET game_balance = ?, main_balance = ? WHERE id = ?', newGameBalance, newMainBalance, userId);

        await db.run(
            'INSERT INTO transactions (user_id, type, amount, signature, status) VALUES (?, ?, ?, ?, ?)',
            userId, 'withdraw', amount, signatureToVerify, 'approved'
        );

        res.json({
            message: 'Withdrawal completed! Transferred to Main Balance.',
            amount,
            gameBalance: newGameBalance,
            mainBalance: newMainBalance
        });
    } catch (error) {
        console.error('Withdraw error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.get('/history', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const db = getDb();

        const transactions = await db.all(`
            SELECT id, type, amount, sig_r, sig_s, msg_hash, status, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        `, userId);

        res.json({ transactions });
    } catch (error) {
        console.error('History error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.post('/approve/:id', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const transactionId = parseInt(req.params.id);
        const adminId = req.userId!;
        const db = getDb();

        const adminUser = await db.get('SELECT role FROM users WHERE id = ?', adminId) as any;
        if (!adminUser || adminUser.role !== 'admin') {
            return res.status(403).json({ error: 'Access denied: Admins only' });
        }

        const tx = await db.get('SELECT * FROM transactions WHERE id = ?', transactionId) as any;
        if (!tx) {
            return res.status(404).json({ error: 'Transaction not found' });
        }

        if (tx.status !== 'pending') {
            return res.status(400).json({ error: 'Transaction already processed' });
        }

        if (tx.type === 'deposit') {
            await db.run('UPDATE users SET game_balance = game_balance + ? WHERE id = ?', tx.amount, tx.user_id);
        }

        await db.run('UPDATE transactions SET status = ? WHERE id = ?', 'approved', transactionId);

        res.json({ message: 'Transaction approved' });
    } catch (error) {
        console.error('Approve error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

export default router;
