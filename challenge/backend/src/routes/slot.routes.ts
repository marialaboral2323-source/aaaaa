import { Router, Response } from 'express';
import { getDb } from '../models/database';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import { spin } from '../services/slot.service';

const router = Router();

router.post('/spin', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const { betAmount } = req.body;
        const userId = req.userId!;

        if (!betAmount || betAmount <= 0) {
            return res.status(400).json({ error: 'Please enter a valid bet amount' });
        }

        const MAX_BET = 100;
        if (betAmount > MAX_BET) {
            return res.status(400).json({ error: `Maximum bet is ${MAX_BET} USD` });
        }

        const db = getDb();

        const user = await db.get('SELECT game_balance, main_balance FROM users WHERE id = ?', userId) as any;
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        if (user.game_balance < betAmount) {
            return res.status(400).json({ error: 'Insufficient game balance' });
        }
        const result = spin(betAmount);

        const netChange = result.payout - betAmount;
        const newGameBalance = user.game_balance + netChange;
        await db.run('UPDATE users SET game_balance = ? WHERE id = ?', newGameBalance, userId);

        await db.run(
            'INSERT INTO games (user_id, bet_amount, symbols, payout) VALUES (?, ?, ?, ?)',
            userId, betAmount, JSON.stringify(result.symbols), result.payout
        );

        res.json({
            ...result,
            betAmount,
            netChange,
            gameBalance: newGameBalance,
            mainBalance: user.main_balance
        });
    } catch (error) {
        console.error('Spin error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

export default router;
