import subprocess
from pathlib import Path


def probe_codec(file_path: str) -> str:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        file_path,
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        return out
    except Exception:
        return ""


def needs_transcode(file_path: str, target_codec: str = "h264") -> bool:
    codec = probe_codec(file_path)
    return codec != target_codec


def create_hls(input_path: str, output_dir: str) -> Path:
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    playlist = out_path / "index.m3u8"

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-codec:v",
        "libx264",
        "-codec:a",
        "aac",
        "-hls_time",
        "6",
        "-hls_list_size",
        "0",
        str(playlist),
    ]
    subprocess.run(cmd, check=True)
    return playlist
