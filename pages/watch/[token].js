import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import Head from "next/head";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import styles from "../../styles/Watch.module.css";

const SITE_NAME = process.env.NEXT_PUBLIC_SITE_NAME || "FileStore";
const BOT_USERNAME = process.env.NEXT_PUBLIC_BOT_USERNAME || "YourFileBot";

export default function WatchPage({ theme, toggleTheme }) {
  const router = useRouter();
  const { token } = router.query;
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const streamUrl = token ? `/api/stream/${token}` : null;
  const downloadUrl = token ? `/api/download/${token}` : null;

  useEffect(() => {
    if (!token) return;
    // Fetch file metadata from API
    fetch(`/api/file-info?token=${token}`)
      .then((r) => r.json())
      .then((d) => {
        if (d.error) throw new Error(d.error);
        setInfo(d);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [token]);

  const isVideo = info?.mime_type?.startsWith("video/");
  const isAudio = info?.mime_type?.startsWith("audio/");
  const isImage = info?.mime_type?.startsWith("image/");

  return (
    <>
      <Head>
        <title>{info?.file_name ?? "File"} — {SITE_NAME}</title>
      </Head>
      <div className={styles.page}>
        <Navbar theme={theme} toggleTheme={toggleTheme} siteName={SITE_NAME} />

        <main className={styles.main}>
          <div className={styles.container}>
            {!token && (
              <TokenEntry />
            )}

            {token && loading && (
              <div className={styles.loadingState}>
                <div className={styles.spinner} />
                <p>Fetching file info…</p>
              </div>
            )}

            {token && error && (
              <div className={styles.errorState}>
                <div className={styles.errorIcon}>⚠️</div>
                <h2>File not found</h2>
                <p>{error}</p>
                <a href="/" className={styles.btnBack}>← Go Home</a>
              </div>
            )}

            {token && !loading && !error && info && (
              <div className={`${styles.fileView} animate-fadeUp`}>
                {/* File header */}
                <div className={styles.fileHeader}>
                  <div className={styles.fileIconLg}>{getMimeIcon(info.mime_type)}</div>
                  <div className={styles.fileMeta}>
                    <h1 className={styles.fileName}>{info.file_name}</h1>
                    <div className={styles.fileTags}>
                      <span className={styles.tag}>{info.mime_type}</span>
                      <span className={styles.tag}>{formatBytes(info.file_size)}</span>
                    </div>
                  </div>
                </div>

                {/* Media player */}
                <div className={styles.playerWrapper}>
                  {isVideo && (
                    <video
                      className={styles.videoPlayer}
                      controls
                      preload="metadata"
                      src={streamUrl}
                    >
                      Your browser does not support video playback.
                    </video>
                  )}
                  {isAudio && (
                    <div className={styles.audioWrapper}>
                      <div className={styles.audioArt}>{getMimeIcon(info.mime_type)}</div>
                      <p className={styles.audioTitle}>{info.file_name}</p>
                      <audio className={styles.audioPlayer} controls preload="metadata" src={streamUrl}>
                        Your browser does not support audio playback.
                      </audio>
                    </div>
                  )}
                  {isImage && (
                    <img className={styles.imagePreview} src={streamUrl} alt={info.file_name} />
                  )}
                  {!isVideo && !isAudio && !isImage && (
                    <div className={styles.noPreview}>
                      <div className={styles.noPreviewIcon}>{getMimeIcon(info.mime_type)}</div>
                      <p>No preview available for this file type.</p>
                    </div>
                  )}
                </div>

                {/* Action buttons */}
                <div className={styles.actions}>
                  <a href={downloadUrl} className={styles.btnDownload} download>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                    Download File
                  </a>
                  <a
                    href={`https://t.me/${BOT_USERNAME}?start=file_${token}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={styles.btnTelegram}
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.12l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.461c.537-.194 1.006.131.833.941z"/>
                    </svg>
                    Open in Telegram
                  </a>
                  <button
                    className={styles.btnCopy}
                    onClick={() => navigator.clipboard.writeText(window.location.href)}
                  >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                    </svg>
                    Copy Link
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>

        <Footer siteName={SITE_NAME} botUsername={BOT_USERNAME} />
      </div>
    </>
  );
}

function TokenEntry() {
  const router = useRouter();
  const [val, setVal] = useState("");
  return (
    <div className={styles.tokenEntry}>
      <h2>Enter a File Token</h2>
      <p>Paste the token from your bot to stream or download the file.</p>
      <div className={styles.tokenRow}>
        <input
          type="text"
          placeholder="Paste token…"
          value={val}
          onChange={(e) => setVal(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && router.push(`/watch/${val.trim()}`)}
        />
        <button onClick={() => router.push(`/watch/${val.trim()}`)}>Open →</button>
      </div>
    </div>
  );
}

function getMimeIcon(mime) {
  if (!mime) return "📄";
  if (mime.startsWith("video/")) return "🎬";
  if (mime.startsWith("audio/")) return "🎵";
  if (mime.startsWith("image/")) return "🖼️";
  if (mime.includes("pdf")) return "📕";
  if (mime.includes("zip") || mime.includes("rar") || mime.includes("7z")) return "🗜️";
  if (mime.includes("word") || mime.includes("document")) return "📝";
  return "📄";
}

function formatBytes(bytes) {
  if (!bytes) return "Unknown size";
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  while (bytes >= 1024 && i < units.length - 1) { bytes /= 1024; i++; }
  return `${bytes.toFixed(2)} ${units[i]}`;
}
