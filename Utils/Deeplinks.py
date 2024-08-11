# from Utils.Defs import run_sell_0
# from Utils.Defs_alt_enter import start_alt_enter
# from Utils.Defs import start_alt_enter
# from Utils.Process_invite_link import process_invite_link
# from Utils.StateMachine import States


async def process_deeplinks(link, state, bot):
    result = '_'
    if 'Начать заново' in link:
        result = 'заново'
        await state.update_data(come_from=result)
        return result
    elif 'start' in link:
        srez = link[7:]  # Обрезаем в нём первые символы '/start '
        if not srez:  # Если строка пустая
            result = 'обычный_запуск'
            await state.update_data(come_from=result)
            return result
        else:
            if 'altenter' in link:
                result = 'альтернативный'
                await state.update_data(come_from=result)
                # await run_sell_0(call, state, bot)
                # await state.set_state(States.alt_start)
                # await start_alt_enter(link, state, bot)
                return result

            elif 'invitelink' in link:
                user_id_inviter = link[17:]  # Обрезаем в нём ещё символы 'invitelink' и получаем id юзера из ссылки
                result = 'invitelink'
                await state.update_data(come_from=result)
                await state.update_data(user_id_inviter=user_id_inviter)
                # await process_invite_link(user_id_inviter, state, bot)
                return result
            else:
                result = srez
                print(result)
                await state.update_data(come_from=result)
                return result

