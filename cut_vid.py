import subprocess
import os
from datetime import datetime


def run_ffmpeg(command):
    try:
        subprocess.run(command, check=True)
        return True
    except FileNotFoundError:
        print("Lỗi: Máy bạn chưa cài đặt FFmpeg hoặc chưa thêm vào PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi thực hiện lệnh FFmpeg: {e}")
        return False


def cut_video_lossless(input_path, start_time, output_path):
    """
    Cắt từ start_time đến hết video bằng cách re-encode.
    Dùng khi cần cắt chính xác từ vị trí không bắt đầu ở keyframe.
    """
    command = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-ss', start_time,
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        output_path
    ]
    print(f"Đang cắt video từ {start_time} đến hết video...")
    if run_ffmpeg(command):
        print(f"--- THÀNH CÔNG! ---")
        print(f"File đã lưu tại: {os.path.abspath(output_path)}")


def cut_video_between(input_path, start_time, end_time, output_path):
    """
    Cắt đoạn video từ start_time đến end_time.
    - Dùng re-encode vì copy stream sẽ bị lỗi khi start_time không trùng keyframe.
    """
    command = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-ss', start_time,
        '-to', end_time,
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        output_path
    ]

    print(f"Đang cắt đoạn video từ {start_time} đến {end_time}...")
    if run_ffmpeg(command):
        print(f"--- THÀNH CÔNG! ---")
        print(f"File đã lưu tại: {os.path.abspath(output_path)}")


# --- CẤU HÌNH Ở ĐÂY ---
file_goc = r"D:\BotEMA\Mori\km-1392_20260819_141938_part-004.mp4"
thoi_diem_bat_dau = "00:01:10"   # Bắt đầu cắt
thoi_diem_ket_thuc = "00:01:15"  # Kết thúc cắt

# Tạo tên file kèm thời gian lưu
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_ket_qua = os.path.join(
    r"D:\BotEMA",
    f"output_cut_{timestamp}.mp4"
)

print(f"File sẽ lưu: {file_ket_qua}")

# Nếu muốn cắt đoạn giữa:
cut_video_between(file_goc, thoi_diem_bat_dau, thoi_diem_ket_thuc, file_ket_qua)

# Nếu muốn cắt từ thời điểm bắt đầu đến hết video thì dùng:
# cut_video_lossless(file_goc, thoi_diem_bat_dau, file_ket_qua)