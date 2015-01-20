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

class tst_qtestperformance_set2 : public QObject
{
    Q_OBJECT

public:
    tst_qtestperformance_set2();

private Q_SLOTS:
    void vidPerfmWarmPlayLatency();
    void vidPerfmVideoLoadTimeMp4();
    void vidPerfmVideoLoadTimeOgv();
    void vidPerfmTimeTakenOnSrcChgHtml5Video();
    void vidPerfmSeekHtml5Video();


public slots:
    void slotMp4VideoLoaded();
    void slotOgvVideoLoaded();
    void slotPlayAgain();
    void slotVideoChanged();
    void slotVideoPlayed();
    void slotVideoSeeked();

private:
    QWebView *m_view;
    QTimer *pollingtimer;
    QTimer *timer;
    int videoLoadTime;
    QVariant resultVideoWebmPlayed;
    QVariant resultVideoPlayed;
    QVariant resultVideoWebmSeeked;
};

tst_qtestperformance_set2::tst_qtestperformance_set2()
{
 m_view = new QWebView;
}

void tst_qtestperformance_set2::vidPerfmVideoLoadTimeMp4()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/loadmp4video.html"));

    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotMp4VideoLoaded()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));
    qDebug() << "Totals: Time taken to load video :: " << videoLoadTime << "ms";
}

void tst_qtestperformance_set2::slotMp4VideoLoaded()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getLoadTime()");
    if(result.toInt() == 0)
    {
    }
    else
    {
        videoLoadTime = result.toInt();
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance_set2::vidPerfmVideoLoadTimeOgv()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/loadogvvideo.html"));

    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotOgvVideoLoaded()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));
    qDebug() << "Totals: Time taken to load Ogg video :: " << videoLoadTime << "ms";
}

void tst_qtestperformance_set2::slotOgvVideoLoaded()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("getLoadTime()");
    if(result.toInt() == 0)
    {
    }
    else
    {
        videoLoadTime = result.toInt();
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance_set2::vidPerfmWarmPlayLatency()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/playAgain.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));
    m_view->page()->mainFrame()->evaluateJavaScript("funPlayAgain()");

    pollingtimer = new QTimer(this);
    connect(pollingtimer, SIGNAL(timeout()), this, SLOT(slotPlayAgain()));
    pollingtimer->start(1000);

    QVERIFY(::waitForSignal(pollingtimer,SIGNAL(destroyed())));

}

void tst_qtestperformance_set2::slotPlayAgain()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingVideo()");
    if(result.toInt() == 0)
    {

    }
    else
    {
        qDebug()<< "Totals: Time taken to play the video again :: " << result.toInt() << " ms";
        pollingtimer->stop();
        pollingtimer->deleteLater();
    }
}

void tst_qtestperformance_set2::vidPerfmTimeTakenOnSrcChgHtml5Video()
{
    m_view = new QWebView;
    resultVideoWebmPlayed=false;

    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testsrcchg.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playWebm()");

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoChanged()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));

    qDebug() << QTime::currentTime();
    QTest::qSleep(5000);
    qDebug() << QTime::currentTime();

    result = m_view->page()->mainFrame()->evaluateJavaScript("changeVideoSrc()");
    qDebug() << "changeVideoSrc Getting the result" << result.toString();

    result = m_view->page()->mainFrame()->evaluateJavaScript("playWebm()");

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoChanged()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    qDebug() << QTime::currentTime();
    QTest::qSleep(5000);
    qDebug() << QTime::currentTime();
    qDebug() << "Totals: Time taken to play video on src change::" <<resultVideoWebmPlayed.toInt()/2 << "ms" <<"\n\r";
}


void tst_qtestperformance_set2::slotVideoChanged()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingWebm()");
    qDebug() << "slotVideoChanged Getting the result" << result.toString();
    if(result.toInt() == 0)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWebmPlayed=resultVideoWebmPlayed.toInt()+result.toInt();
        timer->stop();
        timer->deleteLater();
    }
}

void tst_qtestperformance_set2::vidPerfmSeekHtml5Video()
{
    m_view = new QWebView;
    resultVideoPlayed=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/seekvideo.html"));
    m_view->show();

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playVideo()");
    qDebug() << "playVideo Getting the result" << result.toString();

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoPlayed()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoPlayed.toBool(),"Failure");

    qDebug() << QTime::currentTime();
    QTest::qSleep(5000);
    qDebug() << QTime::currentTime();

    result = m_view->page()->mainFrame()->evaluateJavaScript("seekByTimestamp()");

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoSeeked()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoWebmSeeked.toInt(),"Failure");
    qDebug() << "Totals: Video Seeked Result ::" << resultVideoWebmSeeked.toInt();
}

void tst_qtestperformance_set2::slotVideoPlayed()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingVideo()");
    if(result.toInt() == 0)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "playingVideo Getting the result" << result.toInt();
        qDebug()<< "Stop the timer";
        resultVideoPlayed=result.toInt();
        timer->stop();
        timer->deleteLater();
    }
}

void tst_qtestperformance_set2::slotVideoSeeked()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isSeeking()");
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "isSeeking Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWebmSeeked=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}


QTEST_MAIN(tst_qtestperformance_set2)
#include "tst_qtestperformance_set2.moc"
