import {
  makeWASocket,
  useMultiFileAuthState,
  DisconnectReason
} from '@whiskeysockets/baileys';
  delay,
  DisconnectReason
} from '@whiskeysockets/baileys';
import { createInterface } from 'readline';
import fs from 'fs';

// Terminal I/O setup
const rl = createInterface({ input: process.stdin, output: process.stdout });
const question = (q) => new Promise(res => rl.question(q, res));

// Main async flow
(async () => {
  try {
    // & Step 1: Login
    const { state, saveCreds } = await useMultiFileAuthState('./auth_info');
    const sock = makeWASocket({ auth: state });
    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', update => {
      const { connection, lastDisconnect } = update;
      if (connection === 'close') {
        const shouldReconnect = lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
        console.log('⚠️ Connection closed:', shouldReconnect ? 'reconnecting...' : 'not reconnecting');
        if (shouldReconnect) startBot();
      } else if (connection === 'open') {
        console.log('✅ Logged in!');
      }
    });

    // & Step 2: Ask for inputs
    const multiNumbersRaw = await question('\x1b[1;92m[√] Enter multiple target numbers (comma-separated):\x1b[0m ');
    const numbers = multiNumbersRaw.split(',').map(s => s.trim()).filter(Boolean);

    const groupRaw = await question('\x1b[1;92m[√] Enter multiple group IDs (comma-separated, include "@g.us"):\x1b[0m ');
    const groups = groupRaw.split(',').map(s => s.trim()).filter(Boolean);

    const msg = await question('\x1b[1;33mEnter the message to send:\x1b[0m ');
    const delaySec = parseInt(await question('\x1b[1;33mDelay between messages (in seconds):\x1b[0m '), 10) || 5;
    console.log('\x1b[1;36mStarting message sends now...\x1b[0m\n');

    // & Step 3: Multi-number send
    for (let no of numbers) {
      const jid = no.includes('@') ? no : no + '@s.whatsapp.net';
      try {
        await sock.sendMessage(jid, { text: msg });
        console.log(`✅ Sent to ${jid}`);
      } catch (e) {
        console.log(`\x1b[1;33mError sending to ${jid}: ${e.message}\x1b[0m`);
      }
      await delay(delaySec * 1000);
    }

    // & Step 4: Group send
    for (let grp of groups) {
      try {
        await sock.sendMessage(grp, { text: msg });
        console.log(`✅ Group message sent to ${grp}`);
      } catch (e) {
        console.log(`\x1b[1;33mError sending to group ${grp}: ${e.message}\x1b[0m`);
      }
      await delay(delaySec * 1000);
    }

    console.log('\n\x1b[1;36m🌟 All done!\x1b[0m');
    process.exit(0);

  } catch (err) {
    console.error('\x1b[1;31m[×] Fatal error:\x1b[0m', err);
    process.exit(1);
  }
})();
