#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
#include "../util.h"
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcss3features : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcss3features();

private Q_SLOTS:
    void init();
    /* Multiple columns tests*/
    void css3FuncColumnCount();
    void css3FuncColumnGap();
    void css3FuncColumnRule();      //failed
    void css3FuncColRuleWidth();
    void css3FuncColRuleStyle();
    void css3FuncColRuleColor();
    void css3FuncColumnWidth();
    void css3FuncColumns();         //failed
    void css3FuncColumnSpan();
    /* User interface tests */
    void css3FuncUserAppearance();
    void css3FuncTextResize();
    void css3FuncBoxSizing();
    void css3FuncOutlineOffset();
    /* Font property tests */
    void css3FuncFontFamily();
    void css3FuncFontStyle();
    void css3FuncFontWeight();
    /* Transitions tests */
    void css3FuncTransition();
    void css3FuncTransitionRunning();
    void css3FuncTransitionDuration();
    void css3FuncTransitionTimingFunc();
    void css3FuncTransitionDelay();

public slots:
    void slotTransRunning();
private:
    QWebView * m_view;
    QVariant resultTransition;
    QTimer *timer;

};

tst_qtestcss3features::tst_qtestcss3features()
{

}

void tst_qtestcss3features::init()
{
    m_view = new QWebView;
}

/****** CSS3 Multiple columns feature testcases ******/

/* Function to verify column count */
void tst_qtestcss3features::css3FuncColumnCount()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colCount()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<< result.toInt();

    /* Compare the result with the expected value */
    QCOMPARE(result.toInt(), 4);
}

/* Function to verify column gap */
void tst_qtestcss3features::css3FuncColumnGap()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colGap()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<< result.toInt();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("40px"));
}
/* Function to verify column rule */
void tst_qtestcss3features::css3FuncColumnRule()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colRule()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toInt();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("4px"));
}

/* Function to verify column rule width */
void tst_qtestcss3features::css3FuncColRuleWidth()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colRuleWidth()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("1px"));
}

/* Function to verify column rule style */
void tst_qtestcss3features::css3FuncColRuleStyle()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colRuleStyle()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("dotted"));
}

/* Function to verify column rule color */
void tst_qtestcss3features::css3FuncColRuleColor()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colRuleColor()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(255, 0, 0)"));
}

/* Function to verify column width */
void tst_qtestcss3features::css3FuncColumnWidth()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colWidth()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("200px"));
}

/* Function to verify no of columns */
void tst_qtestcss3features::css3FuncColumns()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns_span.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("numColumns()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("100px 3"));
}

/* Function to verify column span */
void tst_qtestcss3features::css3FuncColumnSpan()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/multiplecolumns_span.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("colspan()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("all"));
}

/***** CSS3 User Interface feature testcases ******/

/* Function to verify user interface - appearance property */
void tst_qtestcss3features::css3FuncUserAppearance()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/userinterface.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("usrAppear()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("button"));
}
/* Function to verify user interface - resizing property */
void tst_qtestcss3features::css3FuncTextResize()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/userinterface.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("txtResize()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("both"));
}

/* Function to verify user interface - box-sizing property */
void tst_qtestcss3features::css3FuncBoxSizing()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/userinterface_box.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("boxSize()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("border-box"));
}

/* Function to verify user interface - outline-offset property */
void tst_qtestcss3features::css3FuncOutlineOffset()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/userinterface_box.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("outlineOff()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("1px"));
}

/****** CSS3 Font feature testcases ******/

/* Function to verify font-family property */
void tst_qtestcss3features::css3FuncFontFamily()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/font_family.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontFam()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("myFirstFont1"));

}

/* Function to verify font-style property */
void tst_qtestcss3features::css3FuncFontStyle()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/font_style.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontSty1()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("italic"));

}
/* Function to verify font-weight property */
void tst_qtestcss3features::css3FuncFontWeight()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/font_style.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontWt()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("bold"));

}

/****** CSS3 transition testcases ******/
/* Function to verify transition property */
void tst_qtestcss3features::css3FuncTransition()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/transitions.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("transProp()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("width"));

}

/* Function to verify if transition is successful */
void tst_qtestcss3features::css3FuncTransitionRunning()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/transitions.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("transRunning()");
    qDebug() << " Getting the result" << result.toString();

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(slotTransRunning()));
    timer->start(1000);

    QVERIFY(::waitForSignal(timer,SIGNAL(destroyed())));

    /* Verify if the result is true */
    QVERIFY(resultTransition.toBool());

}

void tst_qtestcss3features::slotTransRunning()
{
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTransRunning()");
    qDebug()<< "Result is " << result.toInt();

    if(result.toInt() == 100)
    {
        qDebug() << "Continue polling";
    }
    else
    {
        qDebug()<< "Stop the timer";
        resultTransition=true;
        timer->stop();
        timer->deleteLater();
    }
}

/* Function to verify transition property */
void tst_qtestcss3features::css3FuncTransitionDuration()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/transitions.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("transDur()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}

/* Function to verify transition-timing-function property */
void tst_qtestcss3features::css3FuncTransitionTimingFunc()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/transitions.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("transTiming()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("linear"));

}

/* Function to verify transition-delay property */
void tst_qtestcss3features::css3FuncTransitionDelay()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/transitions.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    /* Read till end of file and store the contents in an array */
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }
    /* Parse the document from the byte array and set
     * it as the content of the document */
    m_view->setContent(line,"text/html");

    /* Invoke the javascript function */
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("transDelay()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("2s"));

}

QTEST_MAIN(tst_qtestcss3features)
#include "tst_qtestcss3features.moc"
