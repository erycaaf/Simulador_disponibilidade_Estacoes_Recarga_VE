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

// Calcula o nível final da bateria após recarga
EXPORT float calculate_final_level(float battery_capacity_kwh, float current_level_percent, float charger_power_kw, float charging_minutes) {
    // Validação básica
    if (charger_power_kw <= 0 || battery_capacity_kwh <= 0 || charging_minutes <= 0) {
        return current_level_percent; // Sem alteração
    }

    // Energia fornecida (kWh)
    float energy_added = charger_power_kw * (charging_minutes / 60.0f);

    // Energia atual (kWh)
    float current_kwh = battery_capacity_kwh * (current_level_percent / 100.0f);

    // Novo nível (kWh)
    float new_kwh = current_kwh + energy_added;
    if (new_kwh > battery_capacity_kwh) {
        new_kwh = battery_capacity_kwh;
    }

    // Converte para porcentagem
    float final_percent = (new_kwh / battery_capacity_kwh) * 100.0f;
    return final_percent;
}
