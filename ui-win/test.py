import watchdog
import watchdog.events
import watchdog.observers

OUT_DIR = "..\\engineOut";
FEN_OUT = OUT_DIR + "\\fen.txt";
MOVE_OUT = OUT_DIR + "\\move.txt";

class Handler(watchdog.events.LoggingEventHandler):
    def __init__(self):
        super().__init__();

    # change the on_modified() method to log
    def on_modified(self, event):
        isFen = event.src_path == FEN_OUT;
        path = FEN_OUT if isFen else MOVE_OUT;
        line = "Engine FEN output" if isFen else "Engine move output";
        with open(path, "r") as file:
            global output;
            output = file.readline();
        if (output != ""): # read line modifies the file lol
            line += ": " + output;
            print(line);

class Watcher(watchdog.observers.Observer):
    def __init__(self, handler):
        super().__init__();
        self.schedule(handler, OUT_DIR);
        self.start();

if __name__ == "__main__":
    handle = Handler();
    observer = Watcher(handle);
    
    try:
        while observer.is_alive():
            observer.join(0.5);
    except KeyboardInterrupt:
        print("Closing watch");
        observer.stop();
        observer.join();
