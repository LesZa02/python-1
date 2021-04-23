from application import *


def main():
    root = tk.Tk()
    root.title('tic-tac-toe')
    root.geometry('%dx%d' % (field_w, field_h))
    root.resizable(False, False)
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
