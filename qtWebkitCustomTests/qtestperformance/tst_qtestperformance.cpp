#include <QString>
#include <QtTest>
#include "qwebsettings.h"
#include "qwebview.h"
#include "qwebelement.h"
#include "qwebframe.h"
#include "qwebpage.h"
#include "qnetworkrequest.h"
#include "qwebsettings.h"
#include "../util.h"
#include "time.h"
#include "qnetworkreply.h"
#include "qnetworkdiskcache.h"
#include "qdesktopservices.h"

class tst_qtestperformance : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestperformance();
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
    //Newly Added
    void vidPerfmVideoDownloadTime();
    void vidPerfmPlaybackrate();
    void vidPerfmMultiplevideoload();
    void vidPerfmColdPlayLatency();

public slots:

    //Newly added
    void slotVideoLoaded();
    void slotLoadMultipleVideo();
    void slotVideoPageLoaded();
    void slotVideoPlaybackRateChanged();
    void slotPlayVideo();

private:
    QWebView * m_view;
    QTime timer;
    clock_t c0, c1;
    bool bFlag;
    QTimer *pollingtimer;
    int videoLoadTime;
};

tst_qtestperformance::tst_qtestperformance()
{
}


void tst_qtestperformance::vidPerfmVideoDownloadTime()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videodwnldtime.html"));

    //connect(m_view,SIGNAL(loadFinished(bool)),this,SLOT(slotVideoPageLoaded()));
    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotVideoLoaded()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));
    qDebug() << "Totals: Time taken to load video :: " << videoLoadTime << "ms";
}

void tst_qtestperformance::slotVideoPageLoaded()
{
    qDebug()<<"video got loaded";
}

void tst_qtestperformance::slotVideoLoaded()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getLoadTime()");
    if(result.toInt() == 0)
    {
        qDebug() << "Continue polling";

    }
    else
    {
        videoLoadTime = result.toInt();
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance::vidPerfmPlaybackrate()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videodwnldtime.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playbackDouble()");
    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotVideoPlaybackRateChanged()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));

}


void tst_qtestperformance::slotVideoPlaybackRateChanged()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("timeToPlay()");
    if(result.toInt() == 0)
    {
        qDebug() << "Continue polling";

    }
    else
    {
        float diff = result.toInt();
        qDebug()<< "Totals: Time to play at 2x rate ::" << (float)diff << "ms";
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance::vidPerfmMultiplevideoload()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/loadmultiplevideos.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QTimer time;
    timer.start();

    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotLoadMultipleVideo()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));
    qDebug() << "Totals: Time taken to load all videos ::" << timer.elapsed() << "ms";

}

void tst_qtestperformance::slotLoadMultipleVideo()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("allLoaded()");
    if(result.toBool() == false)
    {

    }
    else
    {
        qDebug()<< "Stop the timer";
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance::vidPerfmColdPlayLatency()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/playhtml5video.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotPlayVideo()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));

}

void tst_qtestperformance::slotPlayVideo()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingVideo()");
    if(result.toInt() == 0)
    {

    }
    else
    {
        qDebug()<< "Totals: Time taken to play the video :: " << result.toInt() << " ms";
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}


QTEST_MAIN(tst_qtestperformance)
#include "tst_qtestperformance.moc"
