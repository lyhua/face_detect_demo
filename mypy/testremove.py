import demo
import os



if __name__ == "__main__":
    remove_path = os.getcwd()
    remove_path = os.path.join(remove_path, "facevedio")
    if os.path.exists(remove_path):
        demo.remove_dir(remove_path)
    else:
        os.mkdir(remove_path)