#include <stdio.h>

// --- INÍCIO DA ADAPTAÇÃO CROSS-PLATFORM ---
// Se estiver no Windows, usa o comando específico da Microsoft
#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    // Se estiver no Linux (Docker), não precisa de prefixo, deixa vazio
    #define EXPORT
#endif
// --- FIM DA ADAPTAÇÃO ---


// Agora usamos a palavra 'EXPORT' em vez de '__declspec(dllexport)'
EXPORT float calculate_charging_time(float battery_capacity_kwh, float current_level_percent, float charger_power_kw) {
    
    // Validação básica para evitar divisão por zero
    if (charger_power_kw <= 0) {
        return -1.0; // Erro
    }

    // Calcula quanta energia falta para encher (em kWh)
    float needed_kwh = battery_capacity_kwh * (1.0f - (current_level_percent / 100.0f));

    // Calcula o tempo em horas
    float time_hours = needed_kwh / charger_power_kw;

    // Retorna em minutos
    return time_hours * 60.0f;
}
