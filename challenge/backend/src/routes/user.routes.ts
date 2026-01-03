import { Router, Response } from 'express';
import { getDb } from '../models/database';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';

const router = Router();

router.get('/stats', authMiddleware, async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.userId!;
        const db = getDb();

        const user = await db.get('SELECT id, email, game_balance, main_balance, created_at FROM users WHERE id = ?', userId) as any;
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        const stats = await db.get(`
      SELECT 
        COUNT(*) as totalGames,
        COALESCE(SUM(bet_amount), 0) as totalBet,
        COALESCE(SUM(payout), 0) as totalPayout
      FROM games WHERE user_id = ?
    `, userId) as any;

        const totalProfit = stats.totalPayout - stats.totalBet;
        const roi = stats.totalBet > 0 ? ((stats.totalPayout - stats.totalBet) / stats.totalBet * 100).toFixed(2) : 0;

        const recentGames = await db.all(`
      SELECT id, bet_amount, symbols, payout, created_at
      FROM games 
      WHERE user_id = ?
      ORDER BY created_at DESC
      LIMIT 10
    `, userId) as any[];

        res.json({
            user: {
                id: user.id,
                email: user.email,
                gameBalance: user.game_balance,
                mainBalance: user.main_balance,
                createdAt: user.created_at
            },
            stats: {
                totalGames: stats.totalGames,
                totalBet: stats.totalBet,
                totalPayout: stats.totalPayout,
                totalProfit,
                roi: `${roi}%`
            },
            recentGames: recentGames.map(game => ({
                ...game,
                symbols: JSON.parse(game.symbols)
            }))
        });
    } catch (error) {
        console.error('Stats error:', error);
        res.status(500).json({ error: 'Server error occurred' });
    }
});

export default router;
