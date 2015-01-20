#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestfps : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestfps();
    
private Q_SLOTS:
    void htmlPerfLoad();

public :
    QWebView *m_view;
};

tst_qtestfps::tst_qtestfps()
{
}

void tst_qtestfps::htmlPerfLoad()
{
    m_view = new QWebView;
    QUrl url = QUrl("qrc:///test.html");
    QString qPath=":"+QString(s_tdkPath)+"/resources/test.html";
    QFile file(qPath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    m_view->show();

    //QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("frameRate()");
    qDebug() << "Totals : Frame Rate for the animation ::" << result.toString();

    QVERIFY(!(result == NULL));

}


QTEST_MAIN(tst_qtestfps)

#include "tst_qtestfps.moc"
