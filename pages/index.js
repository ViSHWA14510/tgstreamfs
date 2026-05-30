import Head from "next/head";
import Link from "next/link";
import { useState } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import styles from "../styles/Home.module.css";

const BOT_USERNAME = process.env.NEXT_PUBLIC_BOT_USERNAME || "YourFileBot";
const SITE_NAME = process.env.NEXT_PUBLIC_SITE_NAME || "FileStore";
const TAGLINE = process.env.NEXT_PUBLIC_SITE_TAGLINE || "Store, Share & Stream Files via Telegram";

export default function Home({ theme, toggleTheme }) {
  const [token, setToken] = useState("");
  const [loading, setLoading] = useState(false);

  const handleOpen = (type) => {
    const t = token.trim();
    if (!t) return;
    const url = type === "stream" ? `/watch/${t}` : `/download/${t}`;
    window.open(url, "_blank");
  };

  return (
    <>
      <Head>
        <title>{SITE_NAME} — {TAGLINE}</title>
      </Head>

      <div className={styles.page}>
        <Navbar theme={theme} toggleTheme={toggleTheme} siteName={SITE_NAME} />

        {/* ── Hero ── */}
        <section className={styles.hero}>
          <div className={styles.heroOrb1} />
          <div className={styles.heroOrb2} />

          <div className={styles.heroContent}>
            <div className={`${styles.badge} animate-fadeUp`}>
              <span className={styles.badgeDot} />
              Powered by Telegram MTProto
            </div>

            <h1 className={`${styles.heroTitle} animate-fadeUp delay-1`}>
              Store. Share.<br />
              <span className={styles.heroAccent}>Stream.</span>
            </h1>

            <p className={`${styles.heroSub} animate-fadeUp delay-2`}>
              Send any file to <strong>@{BOT_USERNAME}</strong> and instantly get a shareable
              Telegram link, a stream URL, and a direct download — all in seconds.
            </p>

            <div className={`${styles.heroCta} animate-fadeUp delay-3`}>
              <a
                href={`https://t.me/${BOT_USERNAME}`}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.btnPrimary}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.941z"/>
                </svg>
                Open Bot in Telegram
              </a>
              <Link href="/watch" className={styles.btnSecondary}>
                Open a File Link
              </Link>
            </div>
          </div>

          {/* Floating file cards */}
          <div className={`${styles.heroVisual} animate-fadeUp delay-4`}>
            <div className={`${styles.floatCard} ${styles.floatCard1} animate-float`}>
              <div className={styles.floatIcon}>🎬</div>
              <div>
                <div className={styles.floatLabel}>video.mp4</div>
                <div className={styles.floatSub}>Streaming • 1.2 GB</div>
              </div>
              <div className={styles.floatStatus}>Live</div>
            </div>
            <div className={`${styles.floatCard} ${styles.floatCard2} animate-float`} style={{animationDelay:"1.2s"}}>
              <div className={styles.floatIcon}>🎵</div>
              <div>
                <div className={styles.floatLabel}>album.zip</div>
                <div className={styles.floatSub}>Download • 340 MB</div>
              </div>
              <div className={styles.floatStatus}>Ready</div>
            </div>
            <div className={`${styles.floatCard} ${styles.floatCard3} animate-float`} style={{animationDelay:"0.6s"}}>
              <div className={styles.floatIcon}>📄</div>
              <div>
                <div className={styles.floatLabel}>docs.pdf</div>
                <div className={styles.floatSub}>Shared • 8 MB</div>
              </div>
              <div className={styles.floatStatus}>Shared</div>
            </div>
          </div>
        </section>

        {/* ── Quick Open ── */}
        <section className={styles.quickOpen}>
          <div className={styles.container}>
            <div className={styles.quickCard}>
              <h2 className={styles.sectionTitle}>Open a File</h2>
              <p className={styles.sectionSub}>Paste a file token from your bot to stream or download it directly.</p>
              <div className={styles.quickRow}>
                <input
                  className={styles.tokenInput}
                  type="text"
                  placeholder="Paste your file token here…"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleOpen("stream")}
                />
                <button
                  className={styles.btnAccent}
                  onClick={() => handleOpen("stream")}
                  disabled={!token.trim()}
                >
                  🎬 Stream
                </button>
                <button
                  className={styles.btnOutline}
                  onClick={() => handleOpen("download")}
                  disabled={!token.trim()}
                >
                  ⬇️ Download
                </button>
              </div>
              <p className={styles.quickHint}>
                Or use the direct URL: <code className={styles.code}>/watch/&lt;token&gt;</code> · <code className={styles.code}>/download/&lt;token&gt;</code>
              </p>
            </div>
          </div>
        </section>

        {/* ── Features ── */}
        <section className={styles.features}>
          <div className={styles.container}>
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Everything you need</h2>
              <p className={styles.sectionSub}>One bot. Infinite files. Zero expiry.</p>
            </div>
            <div className={styles.featureGrid}>
              {FEATURES.map((f, i) => (
                <div key={i} className={`${styles.featureCard} animate-fadeUp`} style={{animationDelay: `${i * 0.08}s`}}>
                  <div className={styles.featureIcon}>{f.icon}</div>
                  <h3 className={styles.featureTitle}>{f.title}</h3>
                  <p className={styles.featureDesc}>{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── How it works ── */}
        <section className={styles.howItWorks}>
          <div className={styles.container}>
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>How it works</h2>
              <p className={styles.sectionSub}>Three steps from file to link.</p>
            </div>
            <div className={styles.steps}>
              {STEPS.map((s, i) => (
                <div key={i} className={styles.step}>
                  <div className={styles.stepNum}>{String(i + 1).padStart(2, "0")}</div>
                  <div className={styles.stepIcon}>{s.icon}</div>
                  <h3 className={styles.stepTitle}>{s.title}</h3>
                  <p className={styles.stepDesc}>{s.desc}</p>
                  {i < STEPS.length - 1 && <div className={styles.stepArrow}>→</div>}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── CTA Banner ── */}
        <section className={styles.ctaBanner}>
          <div className={styles.container}>
            <div className={styles.ctaCard}>
              <div className={styles.ctaOrb} />
              <h2 className={styles.ctaTitle}>Ready to start storing files?</h2>
              <p className={styles.ctaSub}>Open the bot, send a file, and get your links in under 5 seconds.</p>
              <a
                href={`https://t.me/${BOT_USERNAME}`}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.btnPrimaryLg}
              >
                Get Started — It&apos;s Free
              </a>
            </div>
          </div>
        </section>

        <Footer siteName={SITE_NAME} botUsername={BOT_USERNAME} />
      </div>
    </>
  );
}

const FEATURES = [
  { icon: "📨", title: "Telegram File Link", desc: "Get a t.me link that opens directly in Telegram and delivers the file natively — no browser needed." },
  { icon: "🎬", title: "Instant Streaming", desc: "HTTP 206 partial content support means seeking works perfectly in VLC, browsers, and any media player." },
  { icon: "⬇️", title: "Direct Download", desc: "Share a plain URL anyone can click to download the file immediately — no login, no friction." },
  { icon: "🔒", title: "Force Subscribe", desc: "Gate file access behind channel membership. Users must join before they can download or stream." },
  { icon: "♾️", title: "No Expiry", desc: "Files are stored in your private Telegram channel forever — they never expire or get deleted automatically." },
  { icon: "📊", title: "Admin Dashboard", desc: "Broadcast to all users, view stats, and ban/unban abusers directly from Telegram commands." },
];

const STEPS = [
  { icon: "📤", title: "Send a file to the bot", desc: "Any file type — video, audio, document, photo, zip — up to 2 GB." },
  { icon: "⚡", title: "Get three links instantly", desc: "Telegram link, stream URL, and download URL are generated in seconds." },
  { icon: "🌐", title: "Share anywhere", desc: "Paste your links in chats, websites, or social media. Anyone can access them." },
];
