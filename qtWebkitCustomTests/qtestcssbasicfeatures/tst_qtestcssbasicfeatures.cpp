#include <QString>
#include <QtTest>
#include <QWebView>
#include <QWebFrame>
char *s_tdkPath = getenv("TDK_PATH");
class tst_qtestcssbasicfeatures : public QObject
{
    Q_OBJECT
    
public:
    tst_qtestcssbasicfeatures();
    
private Q_SLOTS:
    void init();
    /* CSS background tests */
    void cssFunctBackground();
    void cssFunctBackgroundAttach();
    void cssFunctBackgroundColor();
    void cssFunctBackgroundImage();
    void cssFunctBackgroundPosition();
    void cssFunctBackgroundRepeat();
    /* CSS font tests */
    void cssFunctFont();
    void cssFunctFontFamily();
    void cssFunctFontSize();
    void cssFunctFontVariant();
    /* CSS links tests */
    void cssFunctLinks();
    /* CSS Lists tests */
    void cssFunctListStyleImage();
    void cssFunctListStylePosition();
    void cssFunctListStyleType();
    /* CSS tables tests */
    void cssFunctTableBorderCollapse();
    void cssFunctTableTextAlign();
    void cssFunctTableTextVerticalAlign();
    void cssFunctTableColor();


private:
    QWebView * m_view;
};



tst_qtestcssbasicfeatures::tst_qtestcssbasicfeatures()
{
}

void tst_qtestcssbasicfeatures::init()
{
    m_view = new QWebView;
}

/*****   CSS basic features - Background  ******/
/* Function to verify background property */
void tst_qtestcssbasicfeatures::cssFunctBackground()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/background.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndProp()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(0, 255, 0) url(http://www.w3schools.com/cssref/smiley.gif) no-repeat fixed 50% 50% / auto padding-box border-box"));

}

/* Function to verify background-attachment property */
void tst_qtestcssbasicfeatures::cssFunctBackgroundAttach()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundAttach.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndAttach()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("fixed"));

}
/* Function to verify background-color property */
void tst_qtestcssbasicfeatures::cssFunctBackgroundColor()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundColor.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndColor()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(100, 149, 237)"));

}
/* Function to verify background-image property */
void tst_qtestcssbasicfeatures::cssFunctBackgroundImage()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundImage.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndImage()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("url(http://www.w3schools.com/cssref/paper.gif)"));

}

/* Function to verify background-postion property */
void tst_qtestcssbasicfeatures::cssFunctBackgroundPosition()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundPosition.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndPos()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("50% 50%"));

}

/* Function to verify background-repeat property */
void tst_qtestcssbasicfeatures::cssFunctBackgroundRepeat()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/backgroundRepeat.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("backgndRepeat()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("repeat-y"));

}
/*****   CSS basic features - Fonts ******/
/* Function to verify font property */
void tst_qtestcssbasicfeatures::cssFunctFont()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/font.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontProp()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("italic normal bold 12px/30px Georgia, serif"));

}

/* Function to verify font property */
void tst_qtestcssbasicfeatures::cssFunctFontFamily()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/fontFamily.html";
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
    QCOMPARE(QString(result.toString()), QString("'Times New Roman', Times, serif"));

}

/* Function to verify font-size property */
void tst_qtestcssbasicfeatures::cssFunctFontSize()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/fontSize.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontSz()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("40px"));

}
/* Function to verify font-variant property */
void tst_qtestcssbasicfeatures::cssFunctFontVariant()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/fontVariant.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("fontVar()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("small-caps"));

}

/*****   CSS basic features - Links ******/
/* Function to verify CSS links (a:link) property */
void tst_qtestcssbasicfeatures::cssFunctLinks()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssLinks.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("links()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(255, 0, 0)"));

}

/*****   CSS basic features - Lists ******/

/* Function to verify CSS list style image property */
void tst_qtestcssbasicfeatures::cssFunctListStyleImage()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssListImage.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("listStyImg()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("url(http://www.w3schools.com/cssref/sqpurple.gif)"));

}
/* Function to verify CSS list style position property */
void tst_qtestcssbasicfeatures::cssFunctListStylePosition()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssListPosition.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("listStyPos()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("inside"));

}

/* Function to verify CSS list style type property */
void tst_qtestcssbasicfeatures::cssFunctListStyleType()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssListStyleType.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("listStyType()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("upper-roman"));

}

/*****   CSS basic features - Tables ******/

/* Function to verify CSS table border-collapse property */
void tst_qtestcssbasicfeatures::cssFunctTableBorderCollapse()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssTables.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("tabBorCollapse()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("collapse"));

}


/* Function to verify CSS table text-align property */
void tst_qtestcssbasicfeatures::cssFunctTableTextAlign()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssTables.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("tableTxtAlign()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("right"));

}


/* Function to verify CSS table text vertical-align property */
void tst_qtestcssbasicfeatures::cssFunctTableTextVerticalAlign()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssTables.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("tableTxtAlignVer()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("bottom"));

}


/* Function to verify CSS table color property */
void tst_qtestcssbasicfeatures::cssFunctTableColor()
{
    /* Select the html file to be read */
    QString qPath=":"+QString(s_tdkPath)+"/resources/cssTables.html";
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
    QVariant result = m_view->page()->mainFrame()->evaluateJavaScript("tableColor()");

    /* Get the return value of the function*/
    qDebug()<<"Result:: "<<result.toString();

    /* Compare the result with the expected value */
    QCOMPARE(QString(result.toString()), QString("rgb(255, 255, 255)"));

}
QTEST_MAIN(tst_qtestcssbasicfeatures)

#include "tst_qtestcssbasicfeatures.moc"
