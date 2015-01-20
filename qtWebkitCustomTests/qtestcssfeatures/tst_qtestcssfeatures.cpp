#include <QString>
#include <QtTest>
#include <QWebView>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssfeatures : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssfeatures();
    
private Q_SLOTS:
    void init();
    void cssFunctTransition();
    void cssFunctTransform();
    void cssFunctVisualEffects();
    void cssFunctCSSSelector();
    void cssFunctMediaQuery();
    void cssFunctNegative();

private:
    QWebView* m_view;
};

tst_qtestcssfeatures::tst_qtestcssfeatures()
{
}

/*******************
 *To initialize the variables
 *needed to excute the test cases
 *****************/
void tst_qtestcssfeatures::init()
{
    m_view = new QWebView;
}


/*******************
 *Loads a web page with
 *CSS transition element
 *****************/
void tst_qtestcssfeatures::cssFunctTransition()
{
    QString qPath="qrc://"+QString(s_tdkPath)+"/resources/CSSTransition.html";
    QUrl url = QUrl(qPath);
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));

}


/*******************
 *Loads a web page with
 *CSS transform element
 *****************/
void tst_qtestcssfeatures::cssFunctTransform()
{
    QString qPath="qrc://"+QString(s_tdkPath)+"/resources/CSSTransform.html";
    QUrl url = QUrl(qPath);
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}


/*******************
 *Loads a web page with
 *CSS visual effects
 *****************/
void tst_qtestcssfeatures::cssFunctVisualEffects()
{
    QUrl url = QUrl("http://css-tricks.com/examples/CSS3Clock/");
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}


/*******************
 *Loads a web page with
 *CSS selector element
 *****************/
void tst_qtestcssfeatures::cssFunctCSSSelector()
{
    QUrl url = QUrl("http://webdesign.maratz.com/lab/fancy-checkboxes-and-radio-buttons/demo.html");
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}


/*******************
 *Loads a web page with
 *CSS media query. Based on the
 *device screen size it tries to load the correponding css file.
 *****************/
void tst_qtestcssfeatures::cssFunctMediaQuery()
{
    QUrl url = QUrl("http://nickguthrie.com/embedd_gui/src/qt-everywhere-opensource-src-4.8.4/examples/webkit/webkit-guide/mob_mediaquery.html");
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}


/*******************
 *Loads a web page with
 *CSS media query. Based on the
 *device screen size it tries to load the correponding css file. Fails if the corresponding
 * css file in not available
 *****************/
void tst_qtestcssfeatures::cssFunctNegative()
{
    QString qPath="qrc://"+QString(s_tdkPath)+"/resources/CSSMediaQuery.html";
    QUrl url = QUrl(qPath);
    m_view->load(url);
    m_view->showFullScreen();
    QVERIFY2(!url.isEmpty(),"Failure");
    QVERIFY2(url.isValid(),"Failure");
    QVERIFY(::waitForSignal(m_view, SIGNAL(loadFinished(bool))));
}



QTEST_MAIN(tst_qtestcssfeatures)

#include "tst_qtestcssfeatures.moc"
