#encoding:utf-8
# git@heroku.com:pytest1091.git
import os,time
import time
from flask import Flask,request
from flask import render_template
from ID import upgrade,decode_id
# import md5
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def id():
    data=[]
    if request.method == 'POST':
        WebInput=request.form['getText']
        data.append((u'输入的ID：',WebInput))
        if (len(WebInput)==18 or len(WebInput)==15):
            try:
                ip=request.access_route[0]
                if len(WebInput)==15:
                    WebInput=upgrade(WebInput)
                    data.append((u'升级后的ID：',WebInput))
                data+=map(lambda x,y:(x,unicode(y)),
                        (u'地区：',u'生日：',u'年龄：',u'性别：',u'*编码校验：'),
                        decode_id(WebInput))
                data.append((u'当前IP：',ip))
                text=(u"\r\n".join([u"%s : %s"%(i,j) for i,j in data]))+"\r\ntime:%s\r\nAgent:%s,"%(time.time(),request.user_agent)
                data.append(u'* 注:此项为真的身份证也有可能是伪造的，编码校验并不会核实个人信息。')
            except:
                # print e
                data=[u'无法找到信息。']
        else:
            data=[u'错误的ID格式。']
    return render_template('id.html',
                            title='Decode ID',
                            inputmsg=u'输入18或15位身份证号:',
                            formtitle=u"输出：",
                            errMsg=u"请输入正确的身份证号(0-9,x/X)",
                            data=data)
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    
    port = int(os.environ.get('PORT',0))
    if port:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=5000,debug=True,threaded=True)
