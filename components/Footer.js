import styles from "../styles/Footer.module.css";

export default function Footer({ siteName, botUsername }) {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div className={styles.brand}>
          <span className={styles.logoIcon}>⚡</span>
          <span className={styles.name}>{siteName}</span>
        </div>
        <p className={styles.copy}>
          Built with Pyrogram + Aiohttp + Next.js on Vercel.
          Hosted separately from your bot for maximum performance.
        </p>
        <div className={styles.links}>
          <a href={`https://t.me/${botUsername}`} target="_blank" rel="noopener noreferrer">
            @{botUsername}
          </a>
          <span>·</span>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
      </div>
    </footer>
  );
}
