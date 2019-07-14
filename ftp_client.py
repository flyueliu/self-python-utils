import ftplib
import os
import slfj_logger

logging = slfj_logger.Sl4jLogger()


class FTPClient:
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)
        self.host = host

    def login(self, user, passwd):
        logging.info("ftp client login {}", self.host)
        self.ftp.login(user, passwd)
        self.ftp.set_pasv(False)
        logging.info(self.ftp.welcome)

    def download_file(self, LocalFile, RemoteFile):  # 下载当个文件
        if os.path.exists(LocalFile):
            logging.error("{} exits!", LocalFile)
            return False
        logging.debug("from host:{} download file:{}", self.host, RemoteFile)
        with open(LocalFile, 'wb') as file_handler:
            try:
                self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
                return True
            except Exception as e:
                logging.error("download {} failed", RemoteFile)
                logging.error(e)

        os.remove(LocalFile)
        return False

    def download_file_tree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        logging.info("remoteDir:{}", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        logging.info("RemoteNames :{}", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print(self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(Local):
                    os.makedirs(Local)
                self.download_file_tree(Local, file)
            else:
                self.download_file(Local, file)
        self.ftp.cwd("..")
        return

    def close(self):
        logging.debug("close ftp client host:{}", self.host)
        self.ftp.quit()
