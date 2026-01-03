import { ec as EC } from 'elliptic';
import crypto from 'crypto';

const ec = new EC('secp256k1');

export interface KeyPair {
    publicKey: string;
    privateKey: string;
}

export function generateKeyPair(): KeyPair {
    const keyPair = ec.genKeyPair();
    return {
        publicKey: keyPair.getPublic('hex'),
        privateKey: keyPair.getPrivate('hex')
    };
}

export function generateWalletKey(): string {
    return crypto.randomBytes(32).toString('hex');
}

export function encryptPrivateKey(privateKey: string, password: string): string {
    const salt = crypto.randomBytes(16);
    const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    let encrypted = cipher.update(privateKey, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    return `${salt.toString('hex')}:${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
}

export function decryptPrivateKey(encryptedData: string, password: string): string {
    const [saltHex, ivHex, authTagHex, encrypted] = encryptedData.split(':');
    const salt = Buffer.from(saltHex, 'hex');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');
    const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');

    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
}

export function signMessage(privateKeyHex: string, message: string): string {
    const keyPair = ec.keyFromPrivate(privateKeyHex, 'hex');
    const msgHash = crypto.createHash('sha256').update(message).digest('hex');
    const signature = keyPair.sign(msgHash);
    return signature.toDER('hex');
}

export function verifySignature(publicKeyHex: string, message: string, signatureHex: string): boolean {
    try {
        const key = ec.keyFromPublic(publicKeyHex, 'hex');
        const msgHash = crypto.createHash('sha256').update(message).digest('hex');
        return key.verify(msgHash, signatureHex);
    } catch (error) {
        return false;
    }
}

export function createWithdrawMessage(userId: number, amount: number, timestamp: number): string {
    return `withdraw:${userId}:${amount}:${timestamp}`;
}

export function createDepositReceiptMessage(userId: number, amount: number, timestamp: number, nonce: string): string {
    return `deposit_receipt:${userId}:${amount}:${timestamp}:${nonce}`;
}

const SECP256K1_ORDER = BigInt('0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141');

const SERVER_SECRET = process.env.SERVER_SECRET;
if (!SERVER_SECRET) {
    console.warn('SERVER_SECRET is not set in environment variables! Using insecure default for dev.');
}
const EFFECTIVE_SECRET = SERVER_SECRET || 'AVARITIA';

function generateVulnerableK(seed: number): bigint {
    let state = BigInt(seed);
    const saltBuffer = Buffer.from(EFFECTIVE_SECRET);
    for (let i = 0; i < saltBuffer.length; i++) {
        state = (state + BigInt(saltBuffer[i])) & BigInt('0xFFFFFFFFFFFFFFFF');
    }

    for (let i = 0; i < 8; i++) {
        state ^= state >> BigInt(12);
        state ^= state << BigInt(25);
        state ^= state >> BigInt(27);
        state = (state * BigInt('0x2545F4914F6CDD1D')) & BigInt('0xFFFFFFFFFFFFFFFF');
    }

    let k = state % (SECP256K1_ORDER - BigInt(1)) + BigInt(1);
    return k;
}

function modInverse(a: bigint, m: bigint): bigint {
    let [old_r, r] = [a % m, m];
    let [old_s, s] = [BigInt(1), BigInt(0)];

    while (r !== BigInt(0)) {
        const quotient = old_r / r;
        [old_r, r] = [r, old_r - quotient * r];
        [old_s, s] = [s, old_s - quotient * s];
    }

    return ((old_s % m) + m) % m;
}

export function signMessageWithRS(
    privateKeyHex: string,
    message: string,
    timestampSeed?: number
): { r: string; s: string; signature: string; msgHash: string } {
    const keyPair = ec.keyFromPrivate(privateKeyHex, 'hex');
    const msgHash = crypto.createHash('sha256').update(message).digest('hex');

    const seed = timestampSeed ?? Math.floor(Date.now() / 10);
    const k = generateVulnerableK(seed);

    const G = ec.g;
    const n = ec.n!;
    const d = keyPair.getPrivate();
    const z = BigInt('0x' + msgHash);

    const kPoint = G.mul(k.toString(16));
    const r = BigInt('0x' + kPoint.getX().toString(16)) % BigInt(n.toString());

    const kInv = modInverse(k, SECP256K1_ORDER);
    const dBigInt = BigInt('0x' + d.toString(16));
    const s_raw = (kInv * (z + r * dBigInt)) % SECP256K1_ORDER;

    const halfN = SECP256K1_ORDER / BigInt(2);
    const s = s_raw > halfN ? SECP256K1_ORDER - s_raw : s_raw;

    const signature = keyPair.sign(msgHash);

    return {
        r: r.toString(16).padStart(64, '0'),
        s: s.toString(16).padStart(64, '0'),
        signature: signature.toDER('hex'),
        msgHash: msgHash
    };
}

export function getCurveOrder(): string {
    return SECP256K1_ORDER.toString(16);
}
