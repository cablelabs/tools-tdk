#include <QString>
#include <QtTest>
#include "qwebview.h"
#include "qwebelement.h"
#include "qwebframe.h"
#include "../util.h"

class tst_qtesthtml5features_set3 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features_set3();
    
private Q_SLOTS:
    void init();
    void html5FunControlsVideo();
    void html5FunAutoplayVideo();
    void html5FunPreloadVideo();
    void html5FunLoopVideo();
    void html5FunHeightVideo();
    void html5FunWidthVideo();
	void html5FunDurChangeVideo();
    void html5FunVolumeVideo();
    

private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultVideoDurChange;

public slots:
    void slotVideoDurChange();

};

tst_qtesthtml5features_set3::tst_qtesthtml5features_set3()
{
}

void tst_qtesthtml5features_set3::init()
{
    m_view = new QWebView;
}

void tst_qtesthtml5features_set3::html5FunControlsVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    result = m_view->page()->mainFrame()->evaluateJavaScript("controls()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunAutoplayVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    result = m_view->page()->mainFrame()->evaluateJavaScript("autoplay()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunPreloadVideo()
{
    m_view = new QWebView;
    QVariant result=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    m_view->page()->mainFrame()->evaluateJavaScript("playvideoWebm()");

    result = m_view->page()->mainFrame()->evaluateJavaScript("preload()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunLoopVideo()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("loop()");
    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunHeightVideo()
{
    m_view = new QWebView;
    QVariant result = false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant resultheight = m_view->page()->mainFrame()->evaluateJavaScript("height()");
    if(resultheight.toInt() == 320)
    {
        result = true;
    }

    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunWidthVideo()
{
    m_view = new QWebView;
    QVariant result = false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant resultwidth = m_view->page()->mainFrame()->evaluateJavaScript("width()");
    if(resultwidth.toInt() == 240)
    {
        result = true;
    }

    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunVolumeVideo()
{
    m_view = new QWebView;
    QVariant result = false;
    QVariant volumeSet=0.2;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testControls.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant resultvol = m_view->page()->mainFrame()->evaluateJavaScript("volume()");
    qDebug() << "Getting the result" << resultvol.toFloat() << "Volume Set" << volumeSet.toFloat();
    if(resultvol.toFloat() == volumeSet.toFloat())
    {
        result = true;
    }

    QVERIFY2(result.toBool(),"Failure");
    qDebug() << "Getting the result" << result.toString();
}

void tst_qtesthtml5features_set3::html5FunDurChangeVideo()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/durChg.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoDurChange()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoDurChange.toBool(),"Failure");
}

void tst_qtesthtml5features_set3::slotVideoDurChange()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("durationChange()");
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoDurChange=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

QTEST_MAIN(tst_qtesthtml5features_set3)

#include "tst_qtesthtml5features_set3.moc"
