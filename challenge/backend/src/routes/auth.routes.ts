import { Router, Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { getDb } from '../models/database';
import { authMiddleware, AuthRequest, JWT_SECRET } from '../middleware/auth.middleware';
import { generateKeyPair, generateWalletKey, encryptPrivateKey } from '../services/crypto.service';

const router = Router();

router.post('/register', async (req: Request, res: Response) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ error: 'Please enter email and password' });
        }

        const db = getDb();

        const existingUser = await db.get('SELECT id FROM users WHERE email = ?', email);
        if (existingUser) {
            return res.status(400).json({ error: 'Email already exists' });
        }
        const passwordHash = await bcrypt.hash(password, 10);

        const keyPair = generateKeyPair();
        const walletKey = generateWalletKey();
        const privateKeyEncrypted = encryptPrivateKey(keyPair.privateKey, walletKey);
        const result = await db.run(
            'INSERT INTO users (email, password_hash, game_balance, main_balance, public_key, private_key_encrypted, wallet_key) VALUES (?, ?, ?, ?, ?, ?, ?)',
            email, passwordHash, 0, 0, keyPair.publicKey, privateKeyEncrypted, walletKey
        );

        const token = jwt.sign({ userId: result.lastID }, JWT_SECRET, { expiresIn: '7d' });

        res.status(201).json({
            message: 'Registration complete!',
            token,
            user: {
                id: result.lastID,
                email,
                gameBalance: 0,
                mainBalance: 0,
                publicKey: keyPair.publicKey
            },
            walletKey
        });
    } catch (error) {
        console.error('Register error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.post('/login', async (req: Request, res: Response) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ error: 'Please enter email and password' });
        }

        const db = getDb();
        const user = await db.get('SELECT * FROM users WHERE email = ?', email) as any;
        if (!user) {
            return res.status(401).json({ error: 'Invalid email or password' });
        }

        const isValidPassword = await bcrypt.compare(password, user.password_hash);
        if (!isValidPassword) {
            return res.status(401).json({ error: 'Invalid email or password' });
        }

        const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

        res.json({
            token,
            user: {
                id: user.id,
                email: user.email,
                gameBalance: user.game_balance,
                mainBalance: user.main_balance
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

router.get('/me', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const db = getDb();
        const user = await db.get('SELECT id, email, game_balance, main_balance, created_at FROM users WHERE id = ?', req.userId) as any;
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({
            user: {
                id: user.id,
                email: user.email,
                gameBalance: user.game_balance,
                mainBalance: user.main_balance,
                createdAt: user.created_at
            }
        });
    } catch (error) {
        console.error('Me error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

export default router;
