import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget

BLOCKLIST_PATH = "C:\Windows\System32\drivers\etc\hosts"
WEBSITE_PREFIX = "127.0.0.1\t"
WEBSITE_BLOCKED_MESSAGE = "Website blocked by Website Blocker"

class WebsiteBlocker(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadBlocklist()

    def initUI(self):
        # Set up the GUI layout
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Website URL:"))
        self.websiteInput = QLineEdit()
        hbox1.addWidget(self.websiteInput)
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addWebsite)
        hbox1.addWidget(self.addButton)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Blocked websites:"))
        self.blockedList = QListWidget()
        hbox2.addWidget(self.blockedList)
        self.removeButton = QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeWebsite)
        hbox2.addWidget(self.removeButton)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)
        self.setWindowTitle("Website Blocker")
        self.show()

    def loadBlocklist(self):
        # Load the blocklist from the hosts file
        with open(BLOCKLIST_PATH, "r") as f:
            for line in f:
                if line.startswith(WEBSITE_PREFIX):
                    website = line.split()[1]
                    self.blockedList.addItem(website)

    def saveBlocklist(self):
        # Save the blocklist to the hosts file
        with open(BLOCKLIST_PATH, "r") as f:
            lines = f.readlines()
        with open(BLOCKLIST_PATH, "w") as f:
            for line in lines:
                if not line.startswith(WEBSITE_PREFIX):
                    f.write(line)
            for i in range(self.blockedList.count()):
                website = self.blockedList.item(i).text()
                f.write(f"{WEBSITE_PREFIX}{website} {WEBSITE_BLOCKED_MESSAGE}\n")

    def addWebsite(self):
        # Add a website to the blocklist
        website = self.websiteInput.text().strip()
        if website:
            self.blockedList.addItem(website)
            self.saveBlocklist()
            self.websiteInput.clear()

    def removeWebsite(self):
        # Remove a website from the blocklist
        selected = self.blockedList.selectedItems()
        if selected:
            for item in selected:
                self.blockedList.takeItem(self.blockedList.row(item))
            self.saveBlocklist()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    blocker = WebsiteBlocker()
    sys.exit(app.exec_())
