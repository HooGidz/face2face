import os
from datetime import datetime
from moviepy import VideoFileClip

def merge_audio_from_original(original_path, copy_path, output_dir):
    if not os.path.exists(original_path):
        print(f"Lỗi: Không tìm thấy video gốc tại: {original_path}")
        return
    if not os.path.exists(copy_path):
        print(f"Lỗi: Không tìm thấy video copy tại: {copy_path}")
        return

    # Tạo chuỗi ngày giờ hiện tại (Ví dụ: 20260606_231530)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Tự động tạo tên file đầu ra kèm ngày giờ
    output_filename = f"ghep_tieng_{current_time}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    print("Đang tải các file video...")
    video_original = VideoFileClip(original_path)
    video_copy = VideoFileClip(copy_path)

    audio_original = video_original.audio
    if audio_original is None:
        print("Lỗi: Video gốc không chứa âm thanh!")
        video_original.close()
        video_copy.close()
        return

    print("Đang ghép âm thanh vào video copy...")
    final_video = video_copy.with_audio(audio_original)

    final_video.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac"
    )

    video_original.close()
    video_copy.close()
    final_video.close()
    print(f"Thành công! Video hoàn chỉnh đã lưu tại: {output_path}")

if __name__ == "__main__":
    video_goc = r"D:\BotEMA\Mori\km-1392_20260819_141938_part-005.mp4"
    video_copy = r"D:\BotEMA\output\7fa6ed64.mp4"
    thu_muc_ra = r"D:\BotEMA\output" # Thư mục chứa file đầu ra

    merge_audio_from_original(video_goc, video_copy, thu_muc_ra)