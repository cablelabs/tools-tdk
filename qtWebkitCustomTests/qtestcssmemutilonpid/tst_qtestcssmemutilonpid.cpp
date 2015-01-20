#include <QString>
#include <QtTest>
#include <QWebView>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssmemutilonpid : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssmemutilonpid();
    
private Q_SLOTS:
    void cssPerfmLoadCSSPage();

private:
    QWebView * m_view;
};

tst_qtestcssmemutilonpid::tst_qtestcssmemutilonpid()
{
}

void tst_qtestcssmemutilonpid::cssPerfmLoadCSSPage()
{
    m_view = new QWebView;

    QString qPath=":"+QString(s_tdkPath)+"/resources/keyframeAnimation.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QString pid = QString::number(QApplication::applicationPid());
    qDebug() << "Pid is" << pid;
    QString filename = "/proc/" + pid + "/status";

    QFile statusfile(filename);
    if (!statusfile.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return;
    }

    QByteArray processOutput = statusfile.readAll();
    QString result = processOutput;
    QStringList list = result.split("\n");
    list.removeAll("");
    qDebug() << "Totals : Memory being used by app ::" << list.at(15);
    file.close();

}

QTEST_MAIN(tst_qtestcssmemutilonpid)

#include "tst_qtestcssmemutilonpid.moc"
