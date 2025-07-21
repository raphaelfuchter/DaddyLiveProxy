#SingleInstance force
Persistent

; --- CONFIGURAÇÕES DO USUÁRIO ---
CaminhoDoBat := "C:\Users\RF17\Documents\GitHub\StepDaddyLiveHD-Lives\server.bat"
CaminhoDoIcone := "C:\Users\RF17\Documents\GitHub\StepDaddyLiveHD-Lives\server.ico"
TextoDica := "LivesServer"

; --- LÓGICA DO SCRIPT (VERSÃO CORRIGIDA E SIMPLIFICADA) ---

; Adiciona os itens diretamente ao menu principal da bandeja
A_TrayMenu.Add("server.bat", ExecutarScript)
A_TrayMenu.Add()
A_TrayMenu.Add("Sair", SairDoScript)

; Define as propriedades do menu principal da bandeja
A_TrayMenu.Default := "server.bat" 
A_TrayMenu.Icon := CaminhoDoIcone
A_TrayMenu.Tip := TextoDica
Return

ExecutarScript(*)
{
    Run('"' CaminhoDoBat '"',, "Hide")
}

SairDoScript(*)
{
    ExitApp
}