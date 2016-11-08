from views import main_window

def main():
	root = main_window.GridPaneWindow()
	root.wm_title("WatchTower SNMP Monitor")
	root.mainloop()

if __name__ == '__main__':
    main()  