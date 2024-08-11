def get_email_text_1(IMT, MASS, KCAL_NORM, KCAL_MIN, DIFF_CAL, WATER, PROTEIN, FAT, CARBO):
    email_text_1 = f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
	<meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <title></title>
</head>
<body style="margin:0;padding:0;word-spacing:normal;background-color:#19738d;">
  <div role="article" aria-roledescription="email" lang="en" style="text-size-adjust:100%;-webkit-text-size-adjust:100%;
  -ms-text-size-adjust:100%;background-color:#19738d;">
    <table role="presentation" style="width:100%;border:none;">
      <tr>
        <td align="center" style="padding:0;">

          <table role="presentation" style="width:99%;border:none;border-spacing:0;text-align:left;font-family:Arial,
          sans-serif;font-size:14px;line-height:15px;">
            <tr>
              <td style="padding:5px 5px 5px 5px;text-align:center;font-size:16px;font-weight:bold;">
                <a href="https://t.me/+cGU8F6OyDCwyOGNk" style="text-decoration:none;">
                <img src="https://kofesutra.ru/tmp/KK_Bot_Results_3.png" alt="Logo" 
                style="max-width:100%;height:auto;border:none;text-decoration:none;color:#ffffff;"></a>
              </td>
            </tr>


            <tr>
              <td style="padding:10px;background-color:#ffffff;">

                <p style="margin:10;margin-bottom:10px;font-size:14px;line-height:30px;font-weight:bold;border
                -bottom:2px solid #f0f0f5;color:#19738d;"><b>Как понимать и использовать результаты, которые выдал 
                чат-бот канала Королевы Калорий?</b></p> 

                  <p style="margin:10;">Индекс массы тела: <b>{IMT}</b></p>
                  <p style="margin:10;">Идеальная масса: <b>{MASS}</b> кг</p>
                  <p style="margin:10;">Дневная норма калорий: <b>{KCAL_NORM}</b> ккал</p>
                  <p style="margin:10;">Основной обмен: <b>{KCAL_MIN}</b> ккал</p>
                  <p style="margin:10;">Безопасный диапазон: <b>{DIFF_CAL}</b> ккал</p>
                  <p style="margin:10;">Дневная норма воды: <b>{WATER}</b> л</p>
                  <p style="margin:10;">Норма белков: <b>{PROTEIN}</b> г</p>
                  <p style="margin:10;">Норма жиров: <b>{FAT}</b> г</p>
                  <p style="margin:10;border-bottom:2px solid #f0f0f5;">Норма углеводов: <b>{CARBO}</b> г</p>

                <p style="margin:10;">Итак:
                <b>Индекс массы тела (ИМТ)</b> – это измерение, основанное на соотношении вашего роста и массы тела.</p>
                <p style="margin:10;">Если ваш ИМТ:</p>
                <p style="margin:10;"><b>меньше 18,5</b>, значит вес недостаточный.</p>
                <p style="margin:10;">Риски для здоровья, связанные с недостаточным весом, включают остеопороз, 
                бесплодие и слабую иммунную систему.</p>
                <p style="margin:10;">Недостаток веса также может указывать на расстройство пищевого поведения или 
                другое основное заболевание.</p>

                <p style="margin:10;"><b>от 18,5 до 24,9</b> - нормальный вес.</p>
                <p style="margin:10;">Ваш вес соответствует росту.</p>
                <p style="margin:10;">Достаточное количество жировой ткани обеспечивает стабильную работу всех органов.</p>
                <p style="margin:10;">Если ИМТ близок к верхней границе, нужно взять под контроль питание. За значением 
                24,9 начинается новая, уже опасная грань.</p>

                <p style="margin:10;">Если ваш вес по ИМТ в границах нормы от 18,5 до 24,9, а похудеть вам все равно хочется, 
                то худейте только до 18,5, желательно с увеличением нагрузок на мышцы. </p> 

                <p style="margin:10;"><b>25 или более</b> - избыточный вес.</p>
                <p style="margin:10;">Вы более подвержены риску развития диабета, 
                сердечно-сосудистых заболеваний и некоторых видов рака.</p>

                <p style="margin:10;border-bottom:2px solid #f0f0f5;">Чем выше нормы ваш ИМТ, тем выше риск этих хронических заболеваний.</p>

                <p style="margin:10;"><b>Основной метаболический обмен (ОМО)</b></p> 
                <p style="margin:10;">У нас получились две цифры:</p> 
                <p style="margin:10;"><b>Ваша дневная норма калорий ({KCAL_NORM} ккал)</b> - расcчитана в соответствии с уровнем 
                вашей физической активности.</p> 
                <p style="margin:10;">Это то количество калорий, которое Вы можете съесть, не боясь набрать 
                лишний вес, т.к. они полностью израсходуются организмом.</p> 

                <p style="margin:10;"><b>Ваш основной обмен ({KCAL_MIN} ккал)</b> - такое количество калорий необходимо 
                для поддержания только внутренних процессов организма.</p>
                <p style="margin:10;">Если калорий будет поступать меньше, значит будут нарушаться обменные процессы, 
                а метаболизм замедляться. Это может провоцировать ухудшение вашего здоровья.</p> 

                <p style="margin:10;">Разница между двумя показателями и есть тот <b>безопасный дефицит калорий</b>, 
                который вы можете себе позволить худея без вреда для здоровья.</p> 

                <p style="margin:10;border-bottom:2px solid #f0f0f5;"><b>В Вашем случае это {DIFF_CAL} ккал.</b></p> 


                <p style="margin:10;">На сегодняшний день научные исследования 
                показывают, что сбросить лишний вес можно ТОЛЬКО через создание дефицита калорий. Что это значит? 
                Говоря бухгалтерским языком "приход должен быть меньше, чем расход".</p> 

                <p style="margin:10;"><b>Отсюда следует вывод</b>: Если хотите расстаться с лишним весом, нужно считать 
                калории! Насколько это хлопотно и отнимает много времени возможно вы уже знаете.</p> 

                <p style="margin:10;"><b>Кроме того</b>: Чтобы худеть без вреда для здоровья, питание должно быть 
                сбалансировано по БЖУ (белки, жиры, углеводы) в выверенной именно для вас пропорции.</p> 

                <p style="margin:10;">А это значит, что каждый день придется жонглировать всевозможными таблицами 
                калорийности и составами продуктов. И это еще не полный список дополнительных трудозатрат!</p> 

                <p style="margin:10;">Так что же, теперь даже и не пытаться?</p> 

                <p style="margin:10;">Почему же, если сильно хочешь, выход есть всегда!</p> 

                <p style="margin:10;"><b>Хотите, чтобы всех этих забот у вас не было? А вы бы  худели с комфортом и удовольствием?</b></p> 

                <p style="margin:10;">Если ответ <b>"Да"</b>, то у нас есть для Вас уникальное решение!</p> 

                <p style="margin:10;">Возвращайтесь в <a href="https://t.me/u_m_k_a_bot" style="text-decoration:underline;">UMKA_Bot</a> скорее!</p> 

                </td> </tr> 





            <tr>
              <td style="padding:5px;text-align:center;font-size:14px;background-color:#19738d;color:#cccccc;">
                <p style="margin:0 0 8px 0;">

                <p style="margin:0;line-height:20px;">&reg; Королевы Калорий<br>
                  <a href="https://t.me/+N1x3i9C14kxiZDE0" style="color:#cccccc;text-decoration:underline;">Телеграм канал</a></p>
                   <a href="https://t.me/u_m_k_a_bot" style="color:#cccccc;text-decoration:underline;">Телеграм бот</a></p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
</body>
</html>
    """
    return email_text_1
