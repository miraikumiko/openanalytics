async function getIpAndCountry() {
    try {
        const response = await fetch("https://freeipapi.com/api/json");
        const data = await response.json();
        return {
            ip: data.ipAddress,
            country: data.countryName
        };
    } catch (error) {
        return { ip: "Unknown", country: "Unknown" };
    }
}


const url = "https://analiytics.example.com";
const referrer = document.referrer;
const userAgent = navigator.userAgent;
const pageUrl = window.location.href;
const clientData = await getIpAndCountry();
const data = {
    referrer: referrer,
    user_agent: userAgent,
    page_url: pageUrl,
    ip: clientData.ip,
    country: clientData.country
}


fetch(url, {
    method: "POST",
    headers: {
        "Token": "XXXXXXXX"
    },
    body: JSON.stringify(data)
})