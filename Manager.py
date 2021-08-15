import MultiAccount
import json

class Manager:

    def __init__(self,folderDownload=None,folderDownloadBackups=None):
        self.Accounts=MultiAccount();
        self.Backups=MultiAccount();
        if folderDownload is not None:
            self.Accounts.Downloads=folderDownload;
        if folderDownloadBackups is not None:
            self.Backups.Downloads=folderDownloadBackups;
    
    def Upload(self,fileName,folderMega=None,fileMega=None,removeFileDisk=False):
        result=self.Accounts.Upload(fileName,folderMega,fileMega,removeFileDisk);
        if result is not None:
            result=self.Backups.Upload(fileName,folderMega,fileMega,removeFileDisk);
            isOk=result is not None;
        else:
            isOk=False;
        return isOk;
    
    def GetFileNotFound(self):
        dicFiles={};
        for file in self.Accounts.GetFiles():
            dicFiles[file]=file;
        
        for file in self.Backups.GetFiles():
            if file not in dicFiles:
                yield file;
    
    def RestoreNotFound(self):
        for file in self.GetFileNotFound():
            self.Accounts.Upload(file);


    def CredentialsToJSon(self):
        credentials={
            'Accounts':self.Accounts.LoginCredentials,
            'Backups':self.Backups.LoginCredentials

        };
        return json.dump(credentials);
    def LoadCredentials(self,credentialsJsonString):
        credentials=json.loads(credentialsJsonString);
        for email,password in credentials['Accounts']:
            self.Accounts.AddOrReplace(email,password);
        for email,password in credentials['Backups']:
            self.Backups.AddOrReplace(email,password);

