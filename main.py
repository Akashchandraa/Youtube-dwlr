import flet as ft
import yt_dlp
import asyncio

class DownloaderApp(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_path = None
        self.folder_picker = ft.FilePicker(on_result=self.on_folder_picked)

    def build(self):
        # Add the folder picker to the page
        self.page.overlay.append(self.folder_picker)

        # Header
        header = ft.Container(
            content=ft.Text(
                "🎥 YouTube Video Downloader",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="white",
            ),
            alignment=ft.alignment.center,
            padding=10,
            bgcolor="blue",
            border_radius=10,
        )

        # URL Input
        self.url_input = ft.TextField(
            label="Enter YouTube URLs",
            hint_text="Add one URL per line",
            border_color="blue",
            text_style=ft.TextStyle(size=14),
            multiline=True,
            expand=True,
        )

        # Save Path Display
        self.path_label = ft.Text(
            "Save Path: Not selected",
            color="gray",
            size=14,
            weight=ft.FontWeight.W_400,
        )

        # Select Path Button
        self.select_path_button = ft.ElevatedButton(
            "Select Save Path",
            icon=ft.icons.FOLDER,
            bgcolor="blue",
            color="white",
            on_click=self.select_save_path,
        )

        # Download Button
        self.download_button = ft.ElevatedButton(
            "Download Videos",
            icon=ft.icons.DOWNLOAD,
            bgcolor="green",
            color="white",
            on_click=self.download_videos,
        )

        # Progress Bar
        self.progress_bar = ft.ProgressBar(
            value=0,
            bgcolor="gray",
            color="green",
        )

        # Status Label
        self.status_label = ft.Text(
            "",
            color="green",
            size=16,
            weight=ft.FontWeight.BOLD,
        )

        # Footer
        footer = ft.Container(
            content=ft.Text(
                "© 2024 Developed by Akashchandra Ambula",
                size=12,
                color="gray",
            ),
            alignment=ft.alignment.center,
            padding=10,
            bgcolor="black",
            border_radius=10,
        )

        # Main Card
        main_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.url_input,
                        self.path_label,
                        ft.Row(
                            controls=[self.select_path_button, self.download_button],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        self.progress_bar,
                        self.status_label,
                    ],
                    spacing=20,
                ),
                padding=20,
                border_radius=15,
                bgcolor="white",
                expand=True,
                shadow=ft.BoxShadow(
                    color="#00000030",  # 30% black opacity for shadow
                    blur_radius=15,
                    spread_radius=5,
                ),
            ),
            width=600,
        )

        # Page Layout
        return ft.Column(
            controls=[
                header,
                ft.Container(content=main_card, alignment=ft.alignment.center),
                footer,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

    def select_save_path(self, e):
        # Open the folder picker
        self.folder_picker.get_directory_path()

    def on_folder_picked(self, result):
        if result and result.path:
            self.save_path = result.path
            self.path_label.value = f"Save Path: {self.save_path}"
            self.update()

    async def download_videos(self, e):
        urls = self.url_input.value.strip().splitlines()

        if not urls or not self.save_path:
            self.show_dialog("Error", "Provide URLs and Save Path")
            return

        self.status_label.value = "Downloading..."
        self.progress_bar.value = 0
        self.update()

        for url in urls:
            if url:
                await self.start_download(url)

    async def start_download(self, url):
        ydl_opts = {
            'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'progress_hooks': [self.progress_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.value = "Download completed!"
            self.update()
        except Exception as e:
            self.show_dialog("Error", str(e))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_size = d.get('total_bytes', 0)
            downloaded = d.get('downloaded_bytes', 0)
            progress_percent = (downloaded / total_size) * 100 if total_size else 0
            self.progress_bar.value = progress_percent
            self.update()

    def show_dialog(self, title, message):
        dialog = ft.AlertDialog(
            title=ft.Text(title, weight=ft.FontWeight.BOLD, color="red"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: dialog.close())],
        )
        self.page.dialog = dialog
        dialog.open()


async def main(page):
    app = DownloaderApp()
    page.add(app)


ft.app(target=main)
