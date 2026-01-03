import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import path from 'path';
import crypto from 'crypto';
import bcrypt from 'bcryptjs';
import { generateKeyPair, generateWalletKey, encryptPrivateKey } from '../services/crypto.service';

const dbPath = process.env.DB_PATH || path.join(__dirname, '../../data/slot.db');

let db: Database;

export async function initDatabase() {
  db = await open({
    filename: dbPath,
    driver: sqlite3.Database
  });

  await db.exec('PRAGMA foreign_keys = ON');

  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      role TEXT DEFAULT 'user',
      game_balance REAL DEFAULT 0,
      main_balance REAL DEFAULT 0,
      public_key TEXT,
      private_key_encrypted TEXT,
      wallet_key TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  const tableInfo = await db.all("PRAGMA table_info(users)");
  const hasRole = tableInfo.some(col => col.name === 'role');
  if (!hasRole) {
    await db.exec("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'");
  }

  const adminEmail = 'admin@avaritia.com';
  const adminExists = await db.get('SELECT id FROM users WHERE email = ?', adminEmail);

  if (!adminExists) {
    const randomPassword = crypto.randomBytes(32).toString('hex');
    const adminPass = await bcrypt.hash(randomPassword, 10);
    const keyPair = generateKeyPair();
    const walletKey = generateWalletKey();
    const privateKeyEncrypted = encryptPrivateKey(keyPair.privateKey, walletKey);

    await db.run(
      'INSERT INTO users (email, password_hash, role, game_balance, main_balance, public_key, private_key_encrypted, wallet_key) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
      adminEmail, adminPass, 'admin', 0, 0, keyPair.publicKey, privateKeyEncrypted, walletKey
    );
    console.log(`Admin user seeded: ${adminEmail}`);
    console.log(`Admin password: ${randomPassword}`);
  }

  await db.exec(`
    CREATE TABLE IF NOT EXISTS games (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      bet_amount REAL NOT NULL,
      symbols TEXT NOT NULL,
      payout REAL NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);

  await db.exec(`
    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      type TEXT NOT NULL CHECK(type IN ('deposit', 'withdraw')),
      amount REAL NOT NULL,
      signature TEXT,
      sig_r TEXT,
      sig_s TEXT,
      msg_hash TEXT,
      status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);

  await db.exec(`
    CREATE TABLE IF NOT EXISTS faucet_claims (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      amount REAL NOT NULL,
      sig_r TEXT,
      sig_s TEXT,
      msg_hash TEXT,
      claimed_at DATE DEFAULT (date('now')),
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);

  console.log('Database initialized');
  return db;
}

export function getDb() {
  if (!db) {
    throw new Error('Database not initialized');
  }
  return db;
}
