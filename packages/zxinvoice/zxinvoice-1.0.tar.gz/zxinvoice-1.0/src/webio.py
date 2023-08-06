from datetime import datetime
from chinese_calendar import is_workday
from aip import AipOcr
from pywebio import *
from pywebio.input import *
from pywebio.output import *
from src.utils import *

def main_accountant():
    accountant = None
    while True:
        config(title='财务查询')
        if accountant is None:
            with use_scope('result'):
                data = input_group('', [
                    input("账号", placeholder = '请填写财务人员账号', name = 'Name', type = TEXT, required = True),
                    input("密码", placeholder = '请输入密码', name = 'Password', type = PASSWORD, required = True),
                ])
            accountant = Accountant(data['Name'])
            e = accountant.login(data['Password'])
            # e = accountant.login('')
            with use_scope('result2', clear=True):
                if e['errcode'] < 0:
                    put_text(e['errmsg']).style('color:red')
                    del accountant
                    accountant = None
                    continue
                elif e['role'] != 2:
                    put_text('你不是财务人员，不可登陆').style('color:red')
                    del accountant
                    accountant = None
                    continue
        with use_scope('result2', clear=True):
            data = input_group('', [
                input("批次号", placeholder = '请填写批次号', name = 'BatchNo', type = NUMBER, required = True)
            ])
        with use_scope('result', clear=True):
            tables = []
            errors = []
            index = 0
            error_index = 0
            total_amount = 0
            batch_no = int(data['BatchNo'])
            error_flag = True
            res_arr = []
            while error_flag:
                error_flag = False
                res_arr = accountant.getResultsByBatchNo(batch_no)
                if len(res_arr) == 0:
                    error_index += 1
                    errors.append([error_index, put_text('没有批次号[%d]的记录' % batch_no).style('color:red')])
                    break
                submitter = Submitter(res_arr[0]['Name'])
                for res in res_arr:
                    index += 1
                    res['AmountInFiguers'] = float(res['AmountInFiguers'])
                    total_amount += res['AmountInFiguers']
                    res['InvoiceDateIsWorkday'] = '是' if is_workday(
                        datetime.strptime(res['InvoiceDate'], '%Y-%m-%d').date()) else '否'
                    u = submitter.getFrequencyNum(res['InvoiceDate'])
                    x = submitter.getRepeatNum(res['InvoiceNum'])
                    y = submitter.getConsecutiveNum(res['InvoiceNum'])
                    z = submitter.getNearNum(res['InvoiceNum'])
                    tables.append([
                        index,
                        '****' + res['InvoiceNum'][-4:],
                        res['InvoiceDate'],
                        # res['TotalAmount'],
                        # res['TotalTax'],
                        res['AmountInFiguers'],
                        0 if res['AmountInFiguers'] < 1500 else put_text('1').style('color:red'),
                        0 if res['InvoiceDateIsWorkday'] == '是' else put_text('1').style('color:red'),
                        0 if u < 3 else put_text(u).style('color:red'),
                        0 if x <= 1 else put_text(x).style('color:red'),
                        y if y == 0 else put_text(y).style('color:red'),
                        z if z == 0 else put_text(z).style('color:red'),
                    ])
                del submitter
            if len(res_arr) > 0:
                put_html('<h4>批次号: %d , 总金额: %.2f</h4>' % (batch_no, total_amount))
                put_table(tables,
                          ['序号', '发票号码', '开票日期',
                           # '合计金额', '合计税额',
                           '价税合计', '大额', '节假日', '频繁', '重复', '连号', '接近'])
            if len(errors) > 0:
                put_html('<h4>出错结果</h4>')
                put_table(errors, ['序号', '出错原因'])

def main_submitter():
    # 通用票据识别控制台地址 https://console.bce.baidu.com/ai/#/ai/ocr/overview/index
    # 以下3个参数配置地址 https://console.bce.baidu.com/ai/#/ai/ocr/app/list
    APP_ID = '27972047'
    API_KEY = 'dpGPdVVWQuaqejAmuvMXXKan'
    SECRET_KEY = 'DI2hLvbNyt66oL6bgBFhCKAdRn4WGzbo'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    submitter = None
    while True:
        config(title='上传发票')
        if submitter is None:
            with use_scope('result'):
                data = input_group('', [
                    input("账号", placeholder = '请填写操作员账号', name = 'Name', type = TEXT, required = True),
                    input("密码", placeholder = '请输入密码', name = 'Password', type = PASSWORD, required = True),
                ])
            submitter = Submitter(data['Name'])
            e = submitter.login(data['Password'])
            # e = submitter.login('')
            with use_scope('result2', clear=True):
                if e['errcode'] < 0:
                    put_text(e['errmsg']).style('color:red')
                    del submitter
                    submitter = None
                    continue
        with use_scope('result2', clear=True):
            data = input_group('', [
                file_upload("选择票据文件（可以多选）",
                            name = 'File',
                            placeholder = '请上传图片或PDF票据文件',
                            accept = ['image/*', 'application/pdf'],
                            multiple = True,
                            required = True)
            ])
        with use_scope('result', clear=True):
            res_arr = []
            tables = []
            errors = []
            index = 0
            file_index = 0
            error_index = 0
            total_amount = 0
            for v in data['File']:
                file_index += 1
                put_text('%s 处理中 ' % v['filename']).style('color:black')
                if v['mime_type'].startswith('image'):
                    res = client.vatInvoice(v['content'])
                elif v['mime_type'] == 'application/pdf':
                    res = client.vatInvoicePdf(v['content'])
                else:
                    continue
                if 'words_result' not in res:
                    error_index += 1
                    errors.append([error_index, v['filename'], put_text('不是一个发票文件').style('color:red')])
                    put_text('↑ [E] 不是一个发票文件').style('color:red')
                    continue
                res = res['words_result']
                if len(res['InvoiceNum']) == 0:
                    error_index += 1
                    errors.append([error_index, v['filename'], put_text('发票号识别错误').style('color:red')])
                    put_text('↑ [E] 发票号识别错误').style('color:red')
                    continue
                res['InvoiceDate'] = res['InvoiceDate'].replace('年', '-').replace('月', '-').replace('日', '')
                if not re.match(r'\d{4}-\d{1,2}-\d{1,2}', res['InvoiceDate']):
                    error_index += 1
                    errors.append([error_index, v['filename'], put_text('发票日期识别错误').style('color:red')])
                    put_text('↑ [E] 发票日期识别错误').style('color:red')
                    continue
                # if time.localtime(time.time()).tm_year - int(res['InvoiceDate'][0:4]) > 4:
                if int(res['InvoiceDate'][0:4]) < 2004 or int(res['InvoiceDate'][0:4]) > 2022:
                    error_index += 1
                    errors.append([error_index, v['filename'], put_text('发票日期超出范围(2004,2022)').style('color:red')])
                    put_text('↑ [E] 发票日期超出范围(2004,2022)').style('color:red')
                    continue
                res['AmountInFiguers'] = chinese2digits(res['AmountInWords']) \
                    if is_chinese_digits(res['AmountInWords']) else res['AmountInFiguers']
                if not is_number(res['AmountInFiguers']):
                    error_index += 1
                    errors.append([error_index, v['filename'], put_text('识别的价税合计不是数字').style('color:red')])
                    put_text('↑ [E] 识别的价税合计不是数字').style('color:red')
                    continue
                res['AmountInFiguers'] = float(res['AmountInFiguers'])
                put_text('↑ [E] 识别成功').style('color:blue')
                res['Name'] = submitter.getName()
                res['InvoiceDateIsWorkday'] = '是' if is_workday(
                    datetime.strptime(res['InvoiceDate'], '%Y-%m-%d').date()) else '否'
                res['MachineNum'] = res['MachineNum'] if 'MachineNum' in res else ''
                res['MachineCode'] = res['MachineCode'] if 'MachineCode' in res else ''
                res['CheckCode'] = res['CheckCode'] if 'CheckCode' in res else ''
                total_amount += res['AmountInFiguers']
                res_arr.append(res)
            if len(res_arr) > 0:
                batch_no = submitter.getBatchNo()
                res_arr.sort(key=lambda xx: xx['InvoiceNum'])
            for res in res_arr:
                res['BatchNo'] = batch_no
                submitter.insert(res)
            for res in res_arr:
                index += 1
                u = submitter.getFrequencyNum(res['InvoiceDate'])
                x = submitter.getRepeatNum(res['InvoiceNum'])
                y = submitter.getConsecutiveNum(res['InvoiceNum'])
                z = submitter.getNearNum(res['InvoiceNum'])
                tables.append([
                    index,
                    res['Name'],
                    '****' + res['InvoiceNum'][-4:],
                    res['InvoiceDate'],
                    # res['TotalAmount'],
                    # res['TotalTax'],
                    res['AmountInFiguers'],
                    0 if res['AmountInFiguers'] < 1500 else put_text('1').style('color:red'),
                    0 if res['InvoiceDateIsWorkday'] == '是' else put_text('1').style('color:red'),
                    0 if u < 3 else put_text(u).style('color:red'),
                    0 if x <= 1 else put_text(x).style('color:red'),
                    y if y == 0 else put_text(y).style('color:red'),
                    z if z == 0 else put_text(z).style('color:red'),
                ])
        with use_scope('result', clear=True):
            if len(res_arr) > 0:
                put_html('<h4>批次号: %d , 总金额: %.2f</h4>' % (batch_no, total_amount))
                put_table(tables, ['序号', '上传人', '发票号码', '开票日期',
                                   # '合计金额', '合计税额',
                                   '价税合计', '大额', '节假日', '频繁', '重复', '连号', '接近'])
            if len(errors) > 0:
                put_html('<h4>出错结果</h4>')
                put_table(errors, ['序号', '文件名', '出错原因'])

def start(port = '8080', debug = True):
    Initialize()
    start_server({'submitter': main_submitter, 'accountant': main_accountant}, port=port, debug=debug)