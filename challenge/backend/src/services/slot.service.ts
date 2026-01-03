export interface SpinResult {
    symbols: string[];
    payout: number;
    multiplier: number;
    isWin: boolean;
}

const SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣'];
const WEIGHTS = [30, 25, 20, 15, 8, 2];

const PAYOUTS: { [key: string]: number } = {
    '🍒': 2,
    '🍋': 3,
    '🍊': 5,
    '🍇': 10,
    '💎': 25,
    '7️⃣': 100
};

const TWO_MATCH_MULTIPLIER = 0.5;

function getRandomSymbol(): string {
    const totalWeight = WEIGHTS.reduce((a, b) => a + b, 0);
    let random = Math.random() * totalWeight;

    for (let i = 0; i < SYMBOLS.length; i++) {
        random -= WEIGHTS[i];
        if (random <= 0) {
            return SYMBOLS[i];
        }
    }

    return SYMBOLS[0];
}

export function spin(betAmount: number): SpinResult {
    const symbols = [getRandomSymbol(), getRandomSymbol(), getRandomSymbol()];

    let multiplier = 0;
    let isWin = false;

    if (symbols[0] === symbols[1] && symbols[1] === symbols[2]) {
        multiplier = PAYOUTS[symbols[0]] || 0;
        isWin = true;
    }
    else if (symbols[0] === symbols[1]) {
        multiplier = (PAYOUTS[symbols[0]] || 0) * TWO_MATCH_MULTIPLIER;
        isWin = multiplier > 0;
    }

    const payout = betAmount * multiplier;

    return {
        symbols,
        payout,
        multiplier,
        isWin
    };
}

export function spinWithSeed(betAmount: number, seed: string): SpinResult {
    return spin(betAmount);
}
