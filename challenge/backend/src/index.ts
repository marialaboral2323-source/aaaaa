
import express from 'express';
import cors from 'cors';
import { initDatabase } from './models/database';
import authRoutes from './routes/auth.routes';
import slotRoutes from './routes/slot.routes';
import userRoutes from './routes/user.routes';
import transactionRoutes from './routes/transaction.routes';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

(async () => {
    try {
        await initDatabase();

        app.use('/api/auth', authRoutes);
        app.use('/api/slot', slotRoutes);
        app.use('/api/user', userRoutes);
        app.use('/api/transaction', transactionRoutes);

        app.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
})();

export default app;
