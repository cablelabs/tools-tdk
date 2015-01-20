#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssvisualeffects : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssvisualeffects();
    
private Q_SLOTS:
    void init();
    void css3FuncLoadCssAnimation();
    void css3FuncLoadCssHslColor();
    void css3FuncLoadTextShadow();
    void css3FuncLoadTextOverflow();
    void css3FuncLoadCSSScrollbars();
    void css3FuncLoadCSSlinearGradient();
    void css3FuncLoadCSSRadialGradient();
    void css3FuncLoadCSSReflection();
    void css3FuncLoadBackgroundImage();
    void css3FuncLoadCSSMask();
    /* revisited CSS3 features */
    void css3FuncBorderImage();
    void css3FuncBorderRadius();
    void css3FuncBoxShadow();
    void css3FuncBackgroundClip();
    void css3FuncBackgroundOrigin();
    void css3FuncBackgroundSize();
    void css3FuncTextWordBreak();
    void css3FuncTextWordWrap();
    void css3FuncAnimationName();
    void css3FuncAnimationDuration();
    void css3FuncAnimationTiming();
    void css3FuncAnimationDelay();
    void css3FuncAnimationIteration();
    void css3FuncAnimationDirection();

private:
    QWebView * m_view;
};

tst_qtestcssvisualeffects::tst_qtestcssvisualeffects()
{
}

void tst_qtestcssvisualeffects::init()
{
    m_view = new QWebView;
}

void tst_qtestcssvisualeffects::css3FuncLoadCssAnimation()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/keyframeAnimation.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isAnimationRunning()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadCssHslColor()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/hslColor.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}


void tst_qtestcssvisualeffects::css3FuncLoadTextShadow()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textShadow.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadTextOverflow()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/textOverflow.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");

    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadCSSScrollbars()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/scrollbar.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}


void tst_qtestcssvisualeffects::css3FuncLoadCSSlinearGradient()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/lineargradient.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadCSSRadialGradient()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/radialgradient.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadCSSReflection()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/reflection.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadBackgroundImage()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundImage.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");


    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    qDebug() << "Result obtained :: " << result.toString();
     QVERIFY(result.toBool());
}

void tst_qtestcssvisualeffects::css3FuncLoadCSSMask()
{
    QString qPath=":"+QString(s_tdkPath)+"/resources/overlay.html";
    QFile file(qPath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        return ;
    }
    QByteArray line;
    while (!file.atEnd()) {
        line = file.readAll();
    }

    m_view->setContent(line,"text/html");
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("isTranslated()");
    QVERIFY(result.toBool());
}

/****** Revisited CSS3 features ******/
/* Function to verify border image   property */
void tst_qtestcssvisualeffects::css3FuncBorderImage()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/borderImage.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("borderImg()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());
}

/* Function to verify border-radius property */
void tst_qtestcssvisualeffects::css3FuncBorderRadius()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/borderRadius.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("borderRad()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("25px"));

}
/* Function to verify box-shadow property */
void tst_qtestcssvisualeffects::css3FuncBoxShadow()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/boxShadow.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("boxShad()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(136, 136, 136) 10px 10px 5px 0px"));

}
/* Function to verify background-clip property */
void tst_qtestcssvisualeffects::css3FuncBackgroundClip()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundClip.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndClip()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("border-box"));

}
/* Function to verify background-origin property */
void tst_qtestcssvisualeffects::css3FuncBackgroundOrigin()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundOrigin.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndOrigin()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("content-box"));

}
/* Function to verify background-size property */
void tst_qtestcssvisualeffects::css3FuncBackgroundSize()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundSize.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndSize()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("200px 100px"));

}

/* Function to verify text effects (word-break) property */
void tst_qtestcssvisualeffects::css3FuncTextWordBreak()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/textWordBreak.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("wordBreak()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("break-all"));

}
/* Function to verify text effects (word-wrap) property */
void tst_qtestcssvisualeffects::css3FuncTextWordWrap()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/textWordBreak.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("wordWrap()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("break-word"));

}
/* Function to verify animation-name property */
void tst_qtestcssvisualeffects::css3FuncAnimationName()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animName()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("myanim"));

}
/* Function to verify animation-name property */
void tst_qtestcssvisualeffects::css3FuncAnimationDuration()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animDur()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("5s"));

}

/* Function to verify animation-timing-function property */
void tst_qtestcssvisualeffects::css3FuncAnimationTiming()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animTimingFn()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("linear"));

}
/* Function to verify animation-timing-function property */
void tst_qtestcssvisualeffects::css3FuncAnimationDelay()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animDelay()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("2s"));

}
/* Function to verify animation-iteration-count property */
void tst_qtestcssvisualeffects::css3FuncAnimationIteration()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animIter()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Verify if the result is true */
    QVERIFY(result.toBool());

}
/* Function to verify animation-direction property */
void tst_qtestcssvisualeffects::css3FuncAnimationDirection()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/animations.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("animDir()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("alternate"));

}
QTEST_MAIN(tst_qtestcssvisualeffects)

#include "tst_qtestcssvisualeffects.moc"
