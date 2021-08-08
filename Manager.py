import MultiAccount

class Manager:

    def __init__(self,folderDownload=None,folderDownloadBackUps=None):
        self.Accounts=MultiAccount();
        self.BackUps=MultiAccount();
        if folderDownload is not None:
            self.Accounts.Downloads=folderDownload;
        if folderDownloadBackUps is not None:
            self.BackUps.Downloads=folderDownloadBackUps;
    
    def Upload(self,fileName,folderMega=None,fileMega=None,removeFileDisk=False):
        result=self.Accounts.Upload(fileName,folderMega,fileMega,removeFileDisk);
        if result is not None:
            result=self.BackUps.Upload(fileName,folderMega,fileMega,removeFileDisk);
            isOk=result is not None;
        else:
            isOk=False;
        return isOk;
    
    def GetFileNotFound(self):
        dicFiles={};
        for file in self.Accounts.GetFiles():
            dicFiles[file]=file;
        
        for file in self.BackUps.GetFiles():
            if file not in dicFiles:
                yield file;
    
    def RestoreNotFound(self):
        for file in self.GetFileNotFound():
            self.Accounts.Upload(file);
