# GuitarUp

Программа позволяет рисовать аккорды по заданным через виртуальный интерфейс данным.

## Руководство использования

### Струны

>Имеют три состояния: **OPEN**, **PINCHED**, **MUTED**.
>
>**OPEN** - струна играется открытой.
>**PINCHED** - струна зажата на каком-то ладу.
>**MUTED** - струна не играется и/или заглушена.
>
>Данная версия программа не умеет автоматически изменять состояния струн,
>поэтому пользователь должен сам проставлять необходимые состояния.

### Пальцы

>Пальцы по номерам идут в следующем порядке:
>
>1 - указательный,
>2 - средний,
>3 - безымянный,
>4 - мизинец,
>5 - большой.
>
>Каждый палец можно активировать, прожав Checkbox справа от
>соответствующей струны.
>
>После активации пальца вам станет доступно 3 поля: *String*, *Fret*, *Barre len*.
>
>*String* - номер струны, которую зажимает палец. Если палец зажимает баррэ, то это
>номер самой нижней струны.
>
>*Fret* - номер лада, на котором палец зажимает струну.
>
>*Barre len* - кол-во струн выше выбранной, которое зажимается пальцем. По умолчанию
>стоит 0, что подразумевает отсутствие баррэ.
>
>Если в *Barre len* будет указано неверное значение, то программа вылетит. Если в одном
>из полей *String* или *Fret* останется значение 0, то струна не отрисуется

### Название

>В поле *Name* необходимо указать название аккорда, в будущих версиях будет добавлена его
>отрисовка сверху аккорда. Пока оно влияет только на название файла, в котором сохраниться
>картинка.

### Стартовый лад

>В поле *Start Fret* необходимо указать стартовый лад аккорда, в текущей версии не учитывается
>в итоговой картинке - всегда используется первый лад.

### Кнопки

>*Reset* - сбрасывает все настройки до значений по умолчанию.
>
>*Submit* - рисует настроенный аккорд и сохраняет его в папку chords.

### Хранение

> Все нарисованные аккорды хранятся в папке chords.
