from .view_manager import ViewManager
from .home import ViewHome
from .about import ViewAbout

class Views(ViewManager):

    DEFAULT_VIEW: str = "home"

    def __init__(self, *args):
        super().__init__(*args)

    def view_logic(self):
        self.app.view_current = self.DEFAULT_VIEW
        home = ViewHome(self.app)
        about = ViewAbout(self.app)

        def _update():

            print(self.app.view_current)

            if self.app.view_current == 'home':
                home.game_beat()
            elif self.app.view_current == 'about':
                about.game_beat()
            else:
                home.game_beat()

        return _update