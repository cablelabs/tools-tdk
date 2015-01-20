#include <QString>
#include <QtTest>
#include "qwebview.h"
#include "qwebelement.h"
#include "qwebframe.h"
#include "../util.h"

class tst_qtesthtml5features_set2 : public QObject
{
    Q_OBJECT
    
public:
    tst_qtesthtml5features_set2();
    
private Q_SLOTS:
    void init();
    void html5FunSeekHtml5Video();
    void html5FunChangeSrcHtml5Video();

private:
    QWebView* m_view;
    QTimer *timer;
    QVariant resultVideoWebmPlayed;
    QVariant resultVideoWebmSeeked;

public slots:
    void slotVideoSeeked();
    void slotVideoChanged();
};

tst_qtesthtml5features_set2::tst_qtesthtml5features_set2()
{
}

void tst_qtesthtml5features_set2::init()
{
    m_view = new QWebView;
}

void tst_qtesthtml5features_set2::html5FunChangeSrcHtml5Video()
{
    m_view = new QWebView;
    resultVideoWebmPlayed=false;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/testchgsrcfunc.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playmp4()");
    qDebug() << "changeVideoSrc Getting the result" << result.toString();

   /* qDebug()<< "Current time:: " <<QTime::currentTime();
    sleep(5);
    qDebug()<< "Current time:: " <<QTime::currentTime();
*/
    result = m_view->page()->mainFrame()->evaluateJavaScript("changeVideoSrc()");
    qDebug() << "changeVideoSrc Getting the result" << result.toString();
    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoChanged()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoWebmPlayed.toBool(),"Failure");
}

void tst_qtesthtml5features_set2::slotVideoChanged()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("playingWebm()");
    qDebug() << "slotVideoChanged Getting the result" << result.toString();
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

void tst_qtesthtml5features_set2::html5FunSeekHtml5Video()
{
    m_view = new QWebView;
    QString m_publisherip;
    m_view->load(QUrl(m_publisherip.append((char *)getenv ("RESRC_PUBLISHER_LINK"))+"/videoseek.html"));

    QVERIFY(::waitForSignal(m_view,SIGNAL(loadFinished(bool))));

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotVideoSeeked()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));
    QVERIFY2(resultVideoWebmSeeked.toBool(),"Failure");
    qDebug() << "Getting the result" << resultVideoWebmSeeked.toString();
}

void tst_qtesthtml5features_set2::slotVideoSeeked()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isSeeking()");
    if(result.toBool() == false)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug() << "Getting the result" << result.toString();
        qDebug()<< "Stop the timer";
        resultVideoWebmSeeked=result.toString();
        timer->stop();
        timer->deleteLater();
    }
}

QTEST_MAIN(tst_qtesthtml5features_set2)

#include "tst_qtesthtml5features_set2.moc"
