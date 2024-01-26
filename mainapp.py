import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class FileEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Encryption Application')

        self.label = QLabel('No File Selected')
        self.image_label = QLabel(self)
        self.encrypt_button = QPushButton('Encrypt Image')
        self.decrypt_button = QPushButton('Decrypt Image')
        self.encrypt_text_button = QPushButton('Encrypt Text File')
        self.decrypt_text_button = QPushButton('Decrypt Text File')
        self.random_key_button = QPushButton('Generate Random Key')
        self.save_key_button = QPushButton('Save Key')
        self.load_key_button = QPushButton('Load Key')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.random_key_button)
        layout.addWidget(self.save_key_button)
        layout.addWidget(self.load_key_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.encrypt_text_button)
        layout.addWidget(self.decrypt_text_button)

        self.setLayout(layout)

        self.encrypt_button.clicked.connect(self.encryptFile)
        self.decrypt_button.clicked.connect(self.decryptFile)
        self.encrypt_text_button.clicked.connect(self.encryptTextFile)
        self.decrypt_text_button.clicked.connect(self.decryptTextFile)
        self.random_key_button.clicked.connect(self.generateRandomKey)
        self.save_key_button.clicked.connect(self.saveKey)
        self.load_key_button.clicked.connect(self.loadKey)

    def generateRandomKey(self):
        try:
            self.key = get_random_bytes(16)
            self.label.setText('Random Key Generated: ' + self.key.hex())

        except Exception as e:
            self.label.setText('Error Generating Random Key.')

    def saveKey(self):
        try:
            if hasattr(self, 'key'):
                key_file, _ = QFileDialog.getSaveFileName(self, 'Save Key', 'specialKey', filter='All Files (*)')

                if key_file:
                    with open(key_file, 'wb') as file:
                        file.write(self.key)
                    self.label.setText('Key Successfully Saved: ' + key_file)

                else:
                    self.label.setText('Key Saving Operation Canceled.')

            else:
                raise ValueError("Generate a key first.")

        except ValueError as e:
            self.label.setText(str(e))

    def loadKey(self):
        try:
            key_file, _ = QFileDialog.getOpenFileName(self, 'Load Key', filter='All Files (*)')

            if key_file:
                with open(key_file, 'rb') as file:
                    self.key = file.read()
                self.label.setText('Key Successfully Loaded: ' + key_file)

            else:
                self.label.setText('Key Loading Operation Canceled.')

        except Exception as e:
            self.label.setText('Error Loading Key: ' + str(e))

    def encryptFile(self):
        try:
            if not hasattr(self, 'key'):
                raise ValueError("No key specified. Please generate a random key first.")
            
            input_file, _ = QFileDialog.getOpenFileName(self, 'Select File', filter='PNG Files (*.png);;Text Files (*.txt);;All Files (*)')

            if input_file:
                output_file, _ = QFileDialog.getSaveFileName(self, 'Save Encrypted File', filter='All Files (*)')

                if output_file:
                    self.label.setText('Encrypting File...')
                    self.repaint()

                    cipher = AES.new(self.key, AES.MODE_EAX)
                    with open(input_file, 'rb') as file:
                        plaintext = file.read()

                    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

                    with open(output_file, 'wb') as file:
                        file.write(cipher.nonce)
                        file.write(tag)
                        file.write(ciphertext)

                    self.label.setText('File Encrypted.')

                    # Display the encrypted file
                    encrypted_image = QPixmap(output_file)
                    self.image_label.setPixmap(encrypted_image)

        except ValueError as e:
            self.label.setText(str(e))

    def decryptFile(self):
        try:
            if not hasattr(self, 'key'):
                raise ValueError("No key specified. Please generate a random key first.")
            
            input_file, _ = QFileDialog.getOpenFileName(self, 'Select Encrypted File', filter='All Files (*)')

            if input_file:
                output_file, _ = QFileDialog.getSaveFileName(self, 'Save Decrypted File', filter='All Files (*)')

                if output_file:
                    self.label.setText('Decrypting File...')
                    self.repaint()

                    with open(input_file, 'rb') as file:
                        nonce = file.read(16)
                        tag = file.read(16)
                        ciphertext = file.read()

                    cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
                    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

                    with open(output_file, 'wb') as file:
                        file.write(plaintext)

                    self.label.setText('File Decrypted.')

                    # Display the decrypted file
                    decrypted_image = QPixmap(output_file)
                    self.image_label.setPixmap(decrypted_image)

        except ValueError as e:
            self.label.setText(str(e))

    def encryptTextFile(self):
        try:
            if not hasattr(self, 'key'):
                raise ValueError("No key specified. Please generate a random key first.")
            
            input_file, _ = QFileDialog.getOpenFileName(self, 'Select Text File', filter='Text Files (*.txt);;All Files (*)')

            if input_file:
                output_file, _ = QFileDialog.getSaveFileName(self, 'Save Encrypted Text File', filter='All Files (*)')

                if output_file:
                    self.label.setText('Encrypting Text File...')
                    self.repaint()

                    cipher = AES.new(self.key, AES.MODE_EAX)
                    with open(input_file, 'rb') as file:
                        plaintext = file.read()

                    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

                    with open(output_file, 'wb') as file:
                        file.write(cipher.nonce)
                        file.write(tag)
                        file.write(ciphertext)

                    self.label.setText('Text File Encrypted.')

        except ValueError as e:
            self.label.setText(str(e))

    def decryptTextFile(self):
        try:
            if not hasattr(self, 'key'):
                raise ValueError("No key specified. Please generate a random key first.")
            
            input_file, _ = QFileDialog.getOpenFileName(self, 'Select Encrypted Text File', filter='All Files (*)')

            if input_file:
                output_file, _ = QFileDialog.getSaveFileName(self, 'Save Decrypted Text File', filter='Text Files (*.txt);;All Files (*)')

                if output_file:
                    self.label.setText('Decrypting Text File...')
                    self.repaint()

                    with open(input_file, 'rb') as file:
                        nonce = file.read(16)
                        tag = file.read(16)
                        ciphertext = file.read()

                    cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
                    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

                    with open(output_file, 'wb') as file:
                        file.write(plaintext)

                    self.label.setText('Text File Decrypted.')

        except ValueError as e:
            self.label.setText(str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileEncryptionApp()
    ex.show()
    sys.exit(app.exec_())
