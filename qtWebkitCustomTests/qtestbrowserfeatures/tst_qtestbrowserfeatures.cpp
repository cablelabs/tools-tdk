#include <QString>
#include <QtTest>
#include "qwebview.h"
#include "qwebframe.h"
#include <QNetworkProxyFactory>
#include "qmainwindow.h"
#include "qnetworkaccessmanager.h"
#include "qnetworkreply.h"
#ifdef RDK_PRINT_SUPPORT_ENABLED 
#include <QtPrintSupport/QPrinter>
#endif
#include "../util.h"

class tst_qtestbrowserfeatures : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestbrowserfeatures();
    
private Q_SLOTS:
    void init();
    void browFuncViewsource();
    void browFuncSavepageasimage();
#ifdef RDK_PRINT_SUPPORT_ENABLED
    void browFuncSavepageaspdf();
#endif
public slots:
    void slotsourcedownloaded();

private:
    QWebView * m_view;

};

tst_qtestbrowserfeatures::tst_qtestbrowserfeatures()
{
}


void tst_qtestbrowserfeatures::init()
{
    QUrl url =  QUrl("http://www.google.com/ncr");
    m_view = new QWebView;
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}


void tst_qtestbrowserfeatures::browFuncViewsource()
{
    QNetworkAccessManager* accessManager = m_view->page()->networkAccessManager();
    QNetworkRequest request;
    request.setUrl(m_view->url());
    QNetworkReply* reply = accessManager->get(request);
    connect(reply, SIGNAL(finished()), this, SLOT(slotsourcedownloaded()));
    QVERIFY(::waitForSignal(accessManager, SIGNAL(finished(QNetworkReply*))));
}

void tst_qtestbrowserfeatures::slotsourcedownloaded()
{
    QNetworkReply* reply = qobject_cast<QNetworkReply*>(const_cast<QObject*>(sender()));
    qDebug() << reply->readAll();
}

void tst_qtestbrowserfeatures::browFuncSavepageasimage()
{
    QImage image(m_view->size(),QImage::Format_ARGB32_Premultiplied);
    image.fill(Qt::transparent);
    QPainter p(&image);
    m_view->page()->mainFrame()->render(&p);
    p.end();
    QDir().mkdir("../resources");
    image.save("../resources/webpage.jpg");
    QVERIFY2(!image.isNull(),"Failure");
}
#ifdef RDK_PRINT_SUPPORT_ENABLED
void tst_qtestbrowserfeatures::browFuncSavepageaspdf()
{
    QPrinter printer(QPrinter::HighResolution);
    printer.setOutputFormat(QPrinter::PdfFormat);
    QDir().mkdir("../resources");
    printer.setOutputFileName("../resources/pdfFile.pdf");
    m_view->print(&printer);
    QVERIFY2(printer.isValid(),"Failure");

}
#endif
QTEST_MAIN(tst_qtestbrowserfeatures)

#include "tst_qtestbrowserfeatures.moc"

