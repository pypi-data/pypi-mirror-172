import hashlib
try:
    from pysqlcipher3 import dbapi2 as sqlite
except ImportError:
    import sqlite3 as sqlite

class Initialize:
    def __init__(self):
        self.conn = sqlite.connect('yangbo.db')
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA key='n1c3abph';")
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            Name CHAR(32) UNIQUE NOT NULL, -- 财务人员账号
            Role INT NOT NULL, -- 角色，1、普通员工；2、财务人员；
            Password CHAR(32) NOT NULL,
            CreateTime TEXT NOT NULL   -- 创建时间
        );
        
        ''')
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS batch_no (
            -- BatchNo INTEGER PRIMARY KEY AUTOINCREMENT,
            Name CHAR(32) NOT NULL, -- 上传人账号
            CreateTime TEXT NOT NULL,   -- 上传时间
            FOREIGN KEY(Name) REFERENCES user(Name) ON UPDATE CASCADE ON DELETE CASCADE
        );
        ''')
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS accountant_oplog (
            Name CHAR(32) NOT NULL, -- 财务人员账号
            BatchNo INT NOT NULL,   -- 批次号
            CreateTime TEXT NOT NULL,   -- 操作时间
            FOREIGN KEY(Name) REFERENCES user(Name) ON UPDATE CASCADE ON DELETE CASCADE
        );
        ''')
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS invoice (
            -- _id INTEGER PRIMARY KEY AUTOINCREMENT,
            BatchNo INT NOT NULL,   -- 批次号
            Name CHAR(32) NOT NULL, -- 上传人账号
            CreateTime TEXT NOT NULL,   -- 上传时间
            InvoiceCode TEXT NOT NULL,	-- 发票代码
            InvoiceNum TEXT NOT NULL,	-- 发票号码
            InvoiceDate TEXT NOT NULL,	-- 开票日期
            InvoiceDateIsWorkday CHAR(1) NOT NULL,  -- 开票日期是否是工作日
            ServiceType TEXT NOT NULL,	-- 发票消费类型。不同消费类型输出：餐饮、电器设备、通讯、服务、日用品食品、医疗、交通、其他
            InvoiceType TEXT NOT NULL,	-- 发票种类。不同类型发票输出：普通发票、专用发票、电子普通发票、电子专用发票、通行费电子普票、区块链发票、通用机打电子发票
            InvoiceTypeOrg TEXT NOT NULL,	-- 发票名称
            -- InvoiceCodeConfirm TEXT NOT NULL,	-- 发票代码的辅助校验码，一般业务情景可忽略
            -- InvoiceNumConfirm TEXT NOT NULL,	-- 发票号码的辅助校验码，一般业务情景可忽略
            MachineNum TEXT NOT NULL,	-- 机打号码。仅增值税卷票含有此参数
            MachineCode TEXT NOT NULL,	-- 机器编号。仅增值税卷票含有此参数
            CheckCode TEXT NOT NULL,	-- 校验码。增值税专票无此参数
            PurchaserName TEXT NOT NULL,	-- 购方名称
            PurchaserRegisterNum TEXT NOT NULL,	-- 购方纳税人识别号
            PurchaserAddress TEXT NOT NULL,	-- 购方地址及电话
            PurchaserBank TEXT NOT NULL,	-- 购方开户行及账号
            Password TEXT NOT NULL,	-- 密码区
            Province TEXT NOT NULL,	-- 省
            City TEXT NOT NULL,	-- 市
            SheetNum TEXT NOT NULL,	-- 联次信息。专票第一联到第三联分别输出：第一联：记账联、第二联：抵扣联、第三联：发票联；普通发票第一联到第二联分别输出：第一联：记账联、第二联：发票联
            Agent TEXT NOT NULL,	-- 是否代开
            OnlinePay TEXT NOT NULL,	-- 电子支付标识。仅区块链发票含有此参数
            SellerName TEXT NOT NULL,	-- 销售方名称
            SellerRegisterNum TEXT NOT NULL,	-- 销售方纳税人识别号
            SellerAddress TEXT NOT NULL,	-- 销售方地址及电话
            SellerBank TEXT NOT NULL,	-- 销售方开户行及账号
            TotalAmount TEXT NOT NULL,	-- 合计金额
            TotalTax TEXT NOT NULL,	-- 合计税额
            AmountInWords TEXT NOT NULL,	-- 价税合计(大写)
            AmountInFiguers TEXT NOT NULL,	-- 价税合计(小写)
            Payee TEXT NOT NULL,	-- 收款人
            Checker TEXT NOT NULL,	-- 复核
            NoteDrawer TEXT NOT NULL,	-- 开票人
            Remarks TEXT NOT NULL,	-- 备注
            FOREIGN KEY(Name) REFERENCES user(Name) ON UPDATE CASCADE ON DELETE CASCADE
        );
        ''')
        self.conn.commit()
        self.conn.close()

class User:
    def __init__(self, name, role = 0):
        self.conn = sqlite.connect('yangbo.db')
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA key='n1c3abph';")
        self.name = name
        self.role = role

    def __del__(self):
        self.conn.close()

    def getName(self):
        return self.name

    def getRole(self):
        return self.role

    def login(self, password):
        cursor = self.c.execute("SELECT Password, Role FROM user WHERE Name = '%s'" % self.name)
        rows = cursor.fetchall()
        if len(rows) == 0:
            self.c.execute("INSERT INTO user VALUES('%s', '%s', '%s', 'now');"
                           % (self.name, self.role, hashlib.md5(password.encode(encoding='utf-8')).hexdigest()))
            self.conn.commit()
            cursor = self.c.execute("SELECT last_insert_rowid();")
            if cursor.fetchone()[0] > 0:
                return {'errcode': 1, 'errmsg': '首次登陆', 'role': self.role}    # 首次登陆
            else:
                return {'errcode': -1, 'errmsg': '账号创建失败'}   # 账号创建失败
        else:
            if rows[0][0] == hashlib.md5(password.encode(encoding='utf-8')).hexdigest():
                self.role = rows[0][1]
                return {'errcode': 0, 'role': self.role}
            else:
                return {'errcode': -2, 'errmsg': '密码错误'}   # 密码错误

class Accountant(User):
    def __init__(self, name):
        super().__init__(name, role = 2)

    def getResultsByBatchNo(self, batch_no):
        self.c.execute('''
        INSERT INTO accountant_oplog VALUES ('%s', %d, DATETIME('now'))
        ''' % (self.name, batch_no))
        self.conn.commit()
        cursor = self.c.execute('SELECT * FROM invoice WHERE BatchNo = %d ORDER BY InvoiceNum ASC' % batch_no)
        rows = cursor.fetchall()
        res_arr = []
        for row in rows:
            res_arr.append({
                'BatchNo': row[0],
                'Name': row[1],
                'CreateTime': row[2],
                'InvoiceCode': row[3],
                'InvoiceNum': row[4],
                'InvoiceDate': row[5],
                'InvoiceDateIsWorkday': row[6],
                'ServiceType': row[7],
                'InvoiceType': row[8],
                'InvoiceTypeOrg': row[9],
                'MachineNum': row[10],
                'MachineCode': row[11],
                'CheckCode': row[12],
                'PurchaserName': row[13],
                'PurchaserRegisterNum': row[14],
                'PurchaserAddress': row[15],
                'PurchaserBank': row[16],
                'Password': row[17],
                'Province': row[18],
                'City': row[19],
                'SheetNum': row[20],
                'Agent': row[21],
                'OnlinePay': row[22],
                'SellerName': row[23],
                'SellerRegisterNum': row[24],
                'SellerAddress': row[25],
                'SellerBank': row[26],
                'TotalAmount': row[27],
                'TotalTax': row[28],
                'AmountInWords': row[29],
                'AmountInFiguers': row[30],
                'Payee': row[31],
                'Checker': row[32],
                'NoteDrawer': row[33],
                'Remarks': row[34],
            })
        return res_arr

    # 财务人员查询记录
    def opLog(self, batch_no):
        self.c.execute('''
        INSERT INTO accountant_oplog VALUES ('%s', '%s', DATETIME('now'))
         ''' % (self.name, batch_no))
        self.conn.commit()


class Submitter(User):
    def __init__(self, name):
        super().__init__(name, role = 1)

    # 获取批次号
    def getBatchNo(self):
        self.c.execute('''
        INSERT INTO batch_no VALUES ('%s', DATETIME('now'))
         ''' % self.name)
        self.conn.commit()
        cursor = self.c.execute('SELECT last_insert_rowid();')
        return cursor.fetchone()[0]

    # 判断规则，同一个上传人，发票日期，同一天或者连续2天或者连续3天有大于等于3笔
    def getFrequencyNum(self, date):
        cursor = self.c.execute('''
        SELECT MAX(a, b, c) FROM (
            SELECT COUNT(*) a FROM invoice
            WHERE Name = '{0}' AND ABS(JULIANDAY(InvoiceDate) - JULIANDAY('{1}')) <= 1
        ) a JOIN (
            SELECT COUNT(*) b FROM invoice
            WHERE Name = '{0}' AND JULIANDAY(InvoiceDate) - JULIANDAY('{1}') <= 2 AND InvoiceDate >= '{1}'
        ) b JOIN (
            SELECT COUNT(*) c FROM invoice
            WHERE Name = '{0}' AND JULIANDAY(InvoiceDate) - JULIANDAY('{1}') >= -2 AND InvoiceDate <= '{1}'
        ) c
        '''.format(self.name, date))
        return cursor.fetchone()[0]

    # 查询重复
    def getRepeatNum(self, num):
        cursor = self.c.execute("SELECT COUNT(*) c FROM invoice WHERE InvoiceNum = '%s'" % num)
        return cursor.fetchone()[0]

    # 查询连号
    def getConsecutiveNum(self, num):
        cursor = self.c.execute('SELECT COUNT(*) c FROM invoice WHERE ABS(InvoiceNum - %s) = 1' % num)
        return cursor.fetchone()[0]

    # 查询接近
    def getNearNum(self, num):
        cursor = self.c.execute('SELECT COUNT(*) c FROM invoice WHERE ABS(InvoiceNum - %s) > 1 AND ABS(InvoiceNum - %s) < 10' % (num, num))
        return cursor.fetchone()[0]

    def insert(self, ocr):
        self.c.execute('''
        INSERT INTO invoice VALUES (
            {BatchNo},
            '{Name}',
            DATETIME('now'),
            '{InvoiceCode}',
            '{InvoiceNum}',
            '{InvoiceDate}',
            '{InvoiceDateIsWorkday}',
            '{ServiceType}',
            '{InvoiceType}',
            '{InvoiceTypeOrg}',
            -- '{InvoiceCodeConfirm}',
            -- '{InvoiceNumConfirm}',
            '{MachineNum}',
            '{MachineCode}',
            '{CheckCode}',
            '{PurchaserName}',
            '{PurchaserRegisterNum}',
            '{PurchaserAddress}',
            '{PurchaserBank}',
            '{Password}',
            '{Province}',
            '{City}',
            '{SheetNum}',
            '{Agent}',
            '{OnlinePay}',
            '{SellerName}',
            '{SellerRegisterNum}',
            '{SellerAddress}',
            '{SellerBank}',
            '{TotalAmount}',
            '{TotalTax}',
            '{AmountInWords}',
            '{AmountInFiguers}',
            '{Payee}',
            '{Checker}',
            '{NoteDrawer}',
            '{Remarks}'
        )
        '''.format(**ocr))
        self.conn.commit()