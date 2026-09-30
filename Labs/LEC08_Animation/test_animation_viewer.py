"""Non-graphical checks for Drill #8 frame data and timing rules."""

import struct
import unittest
from unittest.mock import Mock, patch

import animation_viewer as viewer


class AnimationViewerTests(unittest.TestCase):
    def test_four_distinct_animations_with_different_frame_counts(self):
        self.assertEqual([item.name for item in viewer.ANIMATIONS], ["Idle", "Walk", "Run", "Jump"])
        self.assertEqual([len(item.frames) for item in viewer.ANIMATIONS], [6, 10, 9, 14])

    def test_source_rectangles_fit_the_compact_sheet(self):
        viewer.validate_animations(viewer.ANIMATIONS)
        with viewer.SHEET_PATH.open("rb") as sheet:
            header = sheet.read(24)
        self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", header[16:24]), (viewer.SHEET_WIDTH, viewer.SHEET_HEIGHT))

    def test_complex_sheet_uses_varying_frame_widths(self):
        widths = {frame.width for item in viewer.ANIMATIONS for frame in item.frames}
        self.assertGreater(len(widths), 4)

    def test_frame_is_enlarged_and_centered(self):
        image = Mock()
        frame = viewer.IDLE.frames[0]
        with patch.object(viewer, "clear_canvas"), patch.object(viewer, "update_canvas"):
            viewer.draw_frame(image, frame)
        args = image.clip_draw.call_args.args
        self.assertEqual(args[4:6], (400, 300))
        self.assertEqual(args[7], viewer.DISPLAY_HEIGHT)
        self.assertGreaterEqual(args[7], 300)

    def test_each_animation_is_played_five_times_then_paused(self):
        with patch.object(viewer, "play_animation_once", return_value=True) as once:
            with patch.object(viewer, "pause_with_events", return_value=True) as pause:
                self.assertTrue(viewer.play_animation(None, viewer.IDLE))
        self.assertEqual(once.call_count, 5)
        pause.assert_called_once_with(1.0)

    def test_all_animations_repeat_in_order_until_quit(self):
        with patch.object(viewer, "open_canvas"), patch.object(viewer, "close_canvas") as close:
            with patch.object(viewer, "load_image", return_value=Mock()):
                with patch.object(viewer, "play_animation", side_effect=[True] * 8 + [False]) as play:
                    viewer.main()
        self.assertEqual(
            [call.args[1].name for call in play.call_args_list],
            ["Idle", "Walk", "Run", "Jump"] * 2 + ["Idle"],
        )
        close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
