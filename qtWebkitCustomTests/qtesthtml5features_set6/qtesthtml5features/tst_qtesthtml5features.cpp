#include <QString>
#include <QtTest>
#include "qwebview.h"
#include "qwebelement.h"
#include "qwebframe.h"
#include "../util.h"

class tst_qtesthtml5features : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features();
    
private Q_SLOTS:
    void init();
    void html5FunLoadVideoWebm();
    void html5FunBwdPlayVideoWebm();
    void html5FunPauseVideo();
    void html5FunMuteVideo();
    void html5FunFwdDoubleVideo();
    void html5FunFwdHalfVideo();
    void html5FunBwdHalfVideo();

private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultVideoWebmPlayed;

public slots:
    void slotVideoWebmPlayed();
    void slotVideoWebmBwdPlayed();

};

tst_qtesthtml5features::tst_qtesthtml5features()
{
}

void tst_qtesthtml5features::init()
{
    m_view = new QWebView;
}

void tst_qtesthtml5features::html5FunLoadVideoWebm()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));


    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoWebmPlayed()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoWebmPlayed.toBool(),"Failure");
}

void tst_qtesthtml5features::slotVideoWebmPlayed()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingWebm()");
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWebmPlayed=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

void tst_qtesthtml5features::html5FunBwdPlayVideoWebm()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoWebmBwdPlayed()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoWebmPlayed.toBool(),"Failure");
}

void tst_qtesthtml5features::slotVideoWebmBwdPlayed()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingWebmBwd()");
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWebmPlayed=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}
void tst_qtesthtml5features::html5FunMuteVideo()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("mute()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}


void tst_qtesthtml5features::html5FunPauseVideo()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("pause()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features::html5FunFwdDoubleVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    QVariant playbackRate = m_view->page()->mainFrame()->evaluateJavaScript("playbackFwdDouble()");
    if (playbackRate == 2)
    {
        result=true;
    }
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features::html5FunFwdHalfVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    QVariant playbackRate = m_view->page()->mainFrame()->evaluateJavaScript("playbackFwdHalf()");
    if (playbackRate == 0.5)
    {
        result=true;
    }
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features::html5FunBwdHalfVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/controls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    QVariant playbackRate = m_view->page()->mainFrame()->evaluateJavaScript("playbackBwdHalf()");
    if (playbackRate == -0.5)
    {
        result=true;
    }
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

QTEST_MAIN(tst_qtesthtml5features)

#include "tst_qtesthtml5features.moc"
