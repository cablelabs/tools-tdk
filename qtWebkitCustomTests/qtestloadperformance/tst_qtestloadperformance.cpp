#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include <QWebElement>
#include <QNetworkRequest>
#include "../util.h"

class tst_qtestloadperformance : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestloadperformance();
    void examineChildElements(const QWebElement &parentElement)
    {
        QWebElement element = parentElement.firstChild();
        while (!element.isNull()) {

            //qDebug() << "Tag Name :: " << element.tagName();
            examineChildElements(element);

            element = element.nextSibling();
        }
    }
    
private Q_SLOTS:
    void htmlPerfLoadLocalPageTime();
    void htmlPerfReloadLocalPageTime();

    void htmlPerfLoadInternetPageTime();
    void htmlPerfReloadInternetPageTime();

    void htmlPerfCpuUtilization();
    void htmlPerfJsExecutionTime();
    void htmlPerfDomparsingTime();
    void htmlPerfPagepaintingtime();
    void htmlPerfCssloadtime();

    void htmlPerfLoadnetworkrequest();

private:

    QWebView *m_view;
    QTime myTimer;
    QString appPath;
    QNetworkRequest request;
    int loadLocalTime;
    int reloadLocalTime;
    int loadInternetTime;
    int reloadInternetTime;
    float cpuUtil;
    int jsTime;
    int paintTime;
    int parsingTime;
    int cssLoadTime;
    clock_t c0, c1;

public slots:
    void slotLocalPageLoaded();
    void slotLocalPageReloadFinished();

    void slotInternetPageLoaded();
    void slotInternetPageReloadFinished();
   
    void slotLoadLocalFirst();
    void slotLoadInternetFirst();

    void slotPageLoadFinished();
    void slotCssPageLoaded();

    void slotLoadedNetworkRequest();
};

tst_qtestloadperformance::tst_qtestloadperformance()
{
    loadLocalTime       = 0;
    reloadLocalTime     = 0;
    loadInternetTime    = 0;
    reloadInternetTime  = 0;
    cpuUtil             = 0;
    jsTime              = 0;
    parsingTime         = 0;
    paintTime           = 0;
    cssLoadTime         = 0;

    m_view  = new QWebView;
    appPath =  QApplication::applicationDirPath();
    myTimer.start();
}


void tst_qtestloadperformance::htmlPerfLoadLocalPageTime()
{
    QUrl url = QUrl::fromLocalFile(appPath + "/../resources/textstyle.html");
    connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLoadLocalFirst()));
    myTimer.restart();
    m_view->load(url);

    QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);

    for(int index = 0 ; index < 25 ; index++)
    {
        QUrl url = QUrl::fromLocalFile(appPath + "/../resources/borderImage.html");
        connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLocalPageLoaded()));
        myTimer.restart();
        m_view->load(url);

        QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

        disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);

        m_view = NULL;
        delete m_view;

        m_view = new QWebView;
        QUrl secondUrl = QUrl::fromLocalFile(appPath + "/../resources/hslColor.html");
        connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLocalPageLoaded()));
        myTimer.restart();
        m_view->load(secondUrl);

        QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

        disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
    }
    qDebug() << "Totals : Average time taken to load a page :: " << (float)loadLocalTime/50 << "ms";
}

void tst_qtestloadperformance::slotLocalPageLoaded()
{
    int loadLocalTimetemp = myTimer.elapsed(); 
//    qDebug() << "elapsed time ::" << loadLocalTimetemp;
    loadLocalTime += loadLocalTimetemp;
}

void tst_qtestloadperformance::slotLoadLocalFirst()
{
    qDebug() << " Totals : Time taken to load local page in first iteration ::" << myTimer.elapsed() << "ms";
}

void tst_qtestloadperformance::htmlPerfReloadLocalPageTime()
{
    QUrl secondUrl = QUrl::fromLocalFile(appPath + "/../resources/hslColor.html");
    m_view->load(secondUrl);
    waitForSignal(m_view,SIGNAL(loadFinished(bool)));

    connect(m_view,SIGNAL(loadFinished(bool)),SLOT(slotLocalPageReloadFinished()));

    for(int index = 0 ; index < 25 ; index++)
    {
        myTimer.restart();
        m_view->reload();
        QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    }
    qDebug() << "Totals : Average Time taken to reload the page :: " << (float)reloadLocalTime/25 << "ms";
//    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
}

void tst_qtestloadperformance::slotLocalPageReloadFinished()
{
    reloadLocalTime +=  myTimer.elapsed();
}

void tst_qtestloadperformance::htmlPerfLoadInternetPageTime()
{
    QUrl url = QUrl("http://www.google.com");
    connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLoadInternetFirst()));
    myTimer.restart();
    m_view->load(url);
    QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);

    for(int index = 0 ; index < 25 ; index++)
    {
        QUrl url = QUrl("http://www.google.com");
        connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotInternetPageLoaded()));
        myTimer.restart();
        m_view->load(url);

        QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

        disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);

        m_view = NULL;
        delete m_view;

        m_view = new QWebView;
        QUrl secondUrl = QUrl("http://www.w3schools.com/");
        connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotInternetPageLoaded()));
        myTimer.restart();
        m_view->load(secondUrl);

        QVERIFY(waitForSignal(m_view,SIGNAL(loadFinished(bool))));

        disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
    }
    qDebug() << "Totals : Average time taken to load a page :: " << (float)loadInternetTime/50 << "ms";
}

void tst_qtestloadperformance::slotInternetPageLoaded()
{
    loadInternetTime += myTimer.elapsed();
}

void tst_qtestloadperformance::slotLoadInternetFirst()
{
 qDebug() << " Totals : Time taken to load internet page in first iteration ::" << myTimer.elapsed() << "ms";
}

void tst_qtestloadperformance::htmlPerfReloadInternetPageTime()
{
    QUrl secondUrl = QUrl("http://www.google.com");
    connect(m_view,SIGNAL(loadFinished(bool)),SLOT(slotInternetPageReloadFinished()));
    m_view->load(secondUrl);
    waitForSignal(m_view,SIGNAL(loadFinished(bool)));

    for(int index = 0 ; index < 25 ; index++)
    {
        myTimer.restart();
        m_view->reload();
        QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    }
    qDebug() << "Totals : Average Time taken to reload the page :: " << (float)reloadInternetTime/25 << "ms";
}

void tst_qtestloadperformance::slotInternetPageReloadFinished()
{
    reloadInternetTime +=  myTimer.elapsed();
}

void tst_qtestloadperformance::htmlPerfCpuUtilization()
{
    m_view = new QWebView;
    connect(m_view,SIGNAL(loadFinished(bool)),SLOT(slotPageLoadFinished()));

    for(int index = 0; index < 25 ; index++)
    {
        c0 = clock();
        QUrl url = QUrl::fromLocalFile(appPath + "/../resources/borderImageHeavy.html");
        m_view->load(url);
        QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    }
    qDebug() << "Totals: Average CPU Utilization ::" << (float)cpuUtil/25;
}

void tst_qtestloadperformance::slotPageLoadFinished()
{
    c1 = clock();
    float cpu = (float)(c1-c0)/CLOCKS_PER_SEC;
    qDebug() << "Clocks per sec " << cpu;
    cpuUtil += cpu;

}

void tst_qtestloadperformance::htmlPerfJsExecutionTime()
{
    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);

    QUrl secondUrl = QUrl::fromLocalFile(appPath + "/../resources/WebPage.html");
    m_view->load(secondUrl);
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));

    for(int index = 0 ; index < 25 ; index++)
    {
         QTime start;
         start.start();

         m_view->page()->mainFrame()->evaluateJavaScript("myFunction()");
         jsTime += start.elapsed();

    }
    qDebug() << "Totals: Time taken to execute javascript function :: " << (float)jsTime/25 << "ms";
}

void tst_qtestloadperformance::htmlPerfDomparsingTime()
{
    QUrl url = QUrl::fromLocalFile(appPath + "/../resources/borderImageHeavy.html");
    m_view->load(url);
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    QWebFrame *frame = m_view->page()->mainFrame();
    QWebElement document = frame->documentElement();

    for(int index = 0 ; index < 25 ; index++ )
    {
        myTimer.restart();
        examineChildElements(document);
        parsingTime += myTimer.elapsed();
    }
    qDebug() << "Totals: Time taken to parse webpage :: " << (float)parsingTime/25 << "ms";
}

void tst_qtestloadperformance::htmlPerfPagepaintingtime()
{
    QUrl url = QUrl::fromLocalFile(appPath + "/../resources/borderImageHeavy.html");
    m_view->load(url);
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    for(int index = 0 ; index < 25 ; index++ )
    {
        myTimer.restart();
        m_view->show();
        paintTime += myTimer.elapsed();
    }
    qDebug() << "Totals: Time taken to paint a page :: " << (float)paintTime/25 << "ms";
}


void tst_qtestloadperformance::htmlPerfCssloadtime()
{
    disconnect(m_view,SIGNAL(loadFinished(bool)),0,0);
    QUrl url = QUrl::fromLocalFile(appPath + "/../resources/css.html");
    QUrl cssFile = QUrl::fromLocalFile(appPath + "/../resources/style.css");
    connect(m_view,SIGNAL(loadFinished(bool)),SLOT(slotCssPageLoaded()));
    for(int index = 0 ; index < 25 ; index++ )
    {
        m_view->load(url);
        myTimer.restart();
        QWebSettings * settings = m_view->settings();
        settings->setUserStyleSheetUrl(cssFile);
        QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
    }
    qDebug() << "Totals: Time taken to load css features in a page :: " << (float)cssLoadTime/25 << "ms";
}


void tst_qtestloadperformance::slotCssPageLoaded()
{
    cssLoadTime += myTimer.elapsed();
}

void tst_qtestloadperformance::htmlPerfLoadnetworkrequest()
{
    m_view = new QWebView();

    request.setUrl(QUrl("http://camendesign.com/code/video_for_everybody/test.html"));

    myTimer.restart();
    m_view->load(request);
    connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotLoadedNetworkRequest()));
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}

void tst_qtestloadperformance::slotLoadedNetworkRequest()
{
    qDebug() << "Totals: Time taken to load a network request :: " << myTimer.elapsed() << "ms";
}

QTEST_MAIN(tst_qtestloadperformance)

#include "tst_qtestloadperformance.moc"
