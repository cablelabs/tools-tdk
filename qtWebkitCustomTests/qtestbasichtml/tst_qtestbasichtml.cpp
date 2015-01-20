#include <QString>
#include <QtTest>
#include "qwebview.h"
#include "qwebelement.h"
#include "qwebframe.h"
#include "../util.h"

char *s_tdkPath = getenv("TDK_PATH");

class tst_qtestbasichtml : public QObject
{
    Q_OBJECT

public:
    tst_qtestbasichtml();

private Q_SLOTS:
    void init();
    void htmlFuncLoadAudio();
    void htmlFuncLoadSVGImage();
    void htmlFuncLoadCanvas();
    void htmlFuncLoadUnsupportedVideo();
    void htmlFuncLoadEmptyUrl();

private:
    QWebView* m_view;
};


tst_qtestbasichtml::tst_qtestbasichtml(void)
{

}

void tst_qtestbasichtml::init()
{
  m_view = new QWebView;
}


void tst_qtestbasichtml::htmlFuncLoadAudio()
{
    QUrl url = QUrl("http://developer.mozilla.org/@api/deki/files/2926/=AudioTest_(1).ogg");
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}

void tst_qtestbasichtml::htmlFuncLoadSVGImage()
{
    QString qPath="qrc://"+QString(s_tdkPath)+"/resources/SVGSource.html";
    QUrl url = QUrl(qPath);
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}

void tst_qtestbasichtml::htmlFuncLoadCanvas()
{
    QWebSettings::globalSettings()->setAttribute(QWebSettings::PluginsEnabled, true);
    m_view = new QWebView();
    m_view->setHtml("<html><head><h1>Hello World</head></head><body bgcolor='cyan'><canvas id='mycanvas' width='640' height='480' style=''></canvas></body></html>");
    m_view->showFullScreen();


    QWebFrame *frame = m_view->page()->mainFrame();
    QWebElement document = frame->documentElement();

    QVERIFY2(!document.isNull(),"Failure");
    frame->evaluateJavaScript("var b_canvas = document.getElementById('mycanvas'); var b_context = b_canvas.getContext('2d');b_context.fillRect(50, 25, 150, 100);");
}


void tst_qtestbasichtml::htmlFuncLoadUnsupportedVideo()
{
    QString qPath="qrc://"+QString(s_tdkPath)+"/resources/movie.avi";
    QByteArray url = QByteArray(qPath.toLocal8Bit().data());
    QString htmlContent = "<html><body><video width=\"320\" height=\"240\" controls><source  src=" +url+ " type=\"video/avi12\">Your browser does not support the video tag.</video></body></html>";
    m_view->setHtml(htmlContent);
    m_view->showFullScreen();

    QVERIFY2(htmlContent.contains(".avi"),"Failure");
}

void tst_qtestbasichtml::htmlFuncLoadEmptyUrl()
{
    QUrl url = QUrl("");
    m_view->load(url);
    m_view->showFullScreen();

    QVERIFY2(url.isEmpty(),"Failure");
}

QTEST_MAIN(tst_qtestbasichtml)

#include "tst_qtestbasichtml.moc"
