import pygame
import os
import sys
import threading
from time import sleep

class ImageViewer:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.images = self._load_images()
        self.current_image_path = self.images[0]
        self.lock = threading.Lock()
        self.running = True

    def _load_images(self):
        supported_formats = ('.jpg', '.jpeg', '.png')
        files = sorted([
            os.path.join(self.image_dir, f)
            for f in os.listdir(self.image_dir)
            if f.lower().endswith(supported_formats)
        ])
        if not files:
            print("No images found in directory.")
            sys.exit(1)
        return files

    def show_image(self, filename):
        """Switch to a specific image by filename."""
        full_path = os.path.join(self.image_dir, filename)
        if full_path in self.images:
            with self.lock:
                self.current_image_path = full_path
        else:
            print(f"Image {filename} not found in directory.")

    def start(self):
        thread = threading.Thread(target=self._run_pygame_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def _run_pygame_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Image Viewer')
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

            with self.lock:
                image_path = self.current_image_path

            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, screen.get_size())
                screen.blit(image, (0, 0))
                pygame.display.flip()
            except Exception as e:
                print(f"Error displaying {image_path}: {e}")

            clock.tick(30)

        pygame.quit()

# === Usage Example ===
if __name__ == "__main__":
    viewer = ImageViewer("/home/robot/Desktop/robot/robot_app/images/display_images")
    viewer.start()

    # Simulate dynamic switching
    viewer.show_image("happy.jpg")
    sleep(2)
    viewer.show_image("sad.jpg")
    sleep(2)
    viewer.stop()
