from mega import Mega
from os import path

import os



class MultiAccount:

    def __init__(self):
        self.Accounts={};
        self.LoginCredentials={};
        self.Anonimus=self.Mega.login();
        self.Downloads="Downloads";

    def GetAccount(self,email):
        return self.Accounts[email];

    def AddOrReplace(self,email,password):
        self.Accounts[email]=Mega().login(email,password);
        self.LoginCredentials[email]=password;

    def GetTotalSpace(self):
        total=0;
        for _,account in self.Accounts:
            total+=account.get_quota();
        return total;

    def GetTotalSpaceFree(self):
        totalFree=0;
        for _,account in self.Accounts:
            totalFree+=account.get_storage_space();
        return totalFree;

    def GetFirstAccountWithSpace(self,spaceBytes):
        accountWithSpace=None;
        for _,account in self.Accounts:
            if account.get_storage_space() >= spaceBytes:
                accountWithSpace=account;
                break;
        return accountWithSpace;
                    
    def GetFiles(self):
        for _,account in self.Accounts:
            for file in account.get_files():
                yield file;
    
    def Import(self,url,folderMega=None,fileNameMega=None,removeFileDisk=True):
        return self.Upload(self.DownloadUrl(url),folderMega,fileNameMega,removeFileDisk);
  
    def Upload(self,filePath,folderMega=None,fileNameMega=None,removeFileDisk=False):
        fileSize = os.path.getsize(filePath);
        account=self.GetFirstAccountWithSpace(fileSize);
        if account is None:
            uploaded=None;
        else: 
            file= account.upload(filePath,folderMega,fileNameMega); 
            if removeFileDisk:
                os.remove(filePath);
            uploaded= [account,file];
        return uploaded;

    def DownloadUrl(self,url):
        if not path.exists(self.Downloads):
            os.makedirs(self.Downloads);
        return self.Anonimus.download_url(url,self.Downloads);
    def Download(self,fileOrFolderNameMega,folderDisc=None,fileDisc=None):
        accountAndElment=self.Find(fileOrFolderNameMega);
        if accountAndElment is not None:
            path=accountAndElment[0].download(accountAndElment[1],folderDisc,fileDisc);
        else:
            path=None;

        return path;

    def Find(self,fileOrFolderNameMega, excludeDeleted=True):
        accountAndElment=None;
    
        for _,account in self.Accounts:
            element=account.find(fileOrFolderNameMega,excludeDeleted);
            if element is not None:
                accountAndElment=[account,element];
                break;
        return accountAndElment;
    def Rename(self,fileOrFolderNameMegaOld,fileOrFolderNameMegaNew):
        accountAndElment=self.Find(fileOrFolderNameMegaOld);
        success= accountAndElment is not None;
        if success:
            accountAndElment[0].rename(accountAndElment[1],fileOrFolderNameMegaNew);
        return success;

    def GetLink(self,fileOrFolderNameMega):
        element=self.Find(fileOrFolderNameMega);
        if element is not None:
            url=element[0].export(element[1]);
        else:
            url=None;
        return url;    



