// gta6-meme-x-01 entry (Node 22, standard library only): it reads POST.json
// from the repository root, checks it names an X post address, and writes it
// to /output/POST.json, where the gate reads it. That is all the program has
// to do. The entry is the post itself: the meme is posted on X from a public
// account with make.fun (a link or written out) and/or a tag of @makefunai
// and the entrant's play code in its text, POST.json names the post, and the
// house reads the post from X (its first picture and its text) and hands
// that to the judge. Nothing this program writes about the post is judged.
//
// POST.json as shipped holds a placeholder address, so the gate refuses it
// as it stands (valid 0). Replace it with the post's address before submit.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');
const post = JSON.parse(raw) as unknown;
if (typeof post !== 'object' || post === null || Array.isArray(post)) {
  console.error('POST.json must be a JSON object like {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}
const url = (post as Record<string, unknown>).url;
if (typeof url !== 'string' || url.length === 0) {
  console.error('POST.json must carry a "url" string naming the X post');
  process.exit(1);
}
// The gate only accepts a real X post address: https://x.com/<handle>/status/<id>
// (or the same on twitter.com). Refuse the placeholder early so a bad submit
// is caught here, not on the site.
const POST_URL = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/(i\/web\/status\/\d+|[^/]+\/status\/\d+)([/?#].*)?$/;
if (!POST_URL.test(url)) {
  console.error(`POST.json url is not an X post address: ${url}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, 'POST.json'), JSON.stringify({ url }) + '\n', 'utf8');
console.log(`POST.json written for ${url}`);
