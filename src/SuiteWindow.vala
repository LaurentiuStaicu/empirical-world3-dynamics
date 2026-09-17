public class World3Empirical.SuiteWindow : Gtk.ApplicationWindow {
    private const string DATA_DIRECTORY = "/app/share/io.github.laurentiustaicu.World3Empirical/scenarios";
    private const int CALIBRATED_INDICATOR_COUNT = 5;

    private const string[] KEYS = {
        "population",
        "industry_per_capita",
        "food_per_capita",
        "pollution_pressure",
        "human_welfare",
        "industry_total",
        "persistent_pollution_stock",
        "resources_remaining_pct"
    };

    private const string[] LABELS_EN = {
        "World population",
        "Industrial output per capita",
        "Food production per capita",
        "Annual CO₂ emissions (activity proxy)",
        "Human development",
        "Total industrial output",
        "Persistent pollution stock (latent)",
        "Non-renewable resources remaining (latent)"
    };

    private const string[] LABELS_RO = {
        "Populație mondială",
        "Producție industrială pe locuitor",
        "Producție alimentară pe locuitor",
        "Emisii CO₂ anuale (proxy activitate)",
        "Dezvoltare umană",
        "Producție industrială totală",
        "Stoc de poluare persistentă (latent)",
        "Resurse neregenerabile rămase (latent)"
    };

    private const string[] UNITS_EN = {
        "billion people",
        "index, 2015=100",
        "FAO index, 2014–2016=100",
        "flow index, 1990=100",
        "index 0–1",
        "index, 2015=100",
        "World3 index, 1990=100",
        "stock index, BAU 1900=100"
    };

    private const string[] UNITS_RO = {
        "miliarde persoane",
        "indice, 2015=100",
        "indice FAO, 2014–2016=100",
        "indice de flux, 1990=100",
        "indice 0–1",
        "indice, 2015=100",
        "indice World3, 1990=100",
        "indice de stoc, BAU 1900=100"
    };

    private const string[] SOURCES_EN = {
        "World Bank — global population",
        "World Bank — industry / population",
        "FAOSTAT — Food, gross per capita",
        "World Bank / EDGAR — CO₂ proxy",
        "UNDP — Human Development Index",
        "World Bank — total industrial output",
        "World3-03 — modelled persistent stock",
        "World3-03 — modelled non-renewable resources"
    };

    private const string[] SOURCES_RO = {
        "World Bank — populație globală",
        "World Bank — industrie / populație",
        "FAOSTAT — Food, gross per capita",
        "World Bank / EDGAR — proxy CO₂",
        "UNDP — Human Development Index",
        "World Bank — producție industrială totală",
        "World3-03 — stoc persistent modelat",
        "World3-03 — resurse neregenerabile modelate"
    };

    private const string[] SOURCE_URLS = {
        "https://api.worldbank.org/v2/country/WLD/indicator/SP.POP.TOTL",
        "https://api.worldbank.org/v2/country/WLD/indicator/NV.IND.TOTL.KD",
        "https://www.fao.org/faostat/en/#data/QI",
        "https://edgar.jrc.ec.europa.eu/dataset_ghg2025",
        "https://hdr.undp.org/data-center/documentation-and-downloads",
        "https://api.worldbank.org/v2/country/WLD/indicator/NV.IND.TOTL.KD",
        "https://web.mit.edu/jsterman/www/DID.html",
        "https://web.mit.edu/jsterman/www/DID.html"
    };

    private const string[] STATUSES_EN = {
        "Observations through 2025; the 2025 value may be an estimate.",
        "Observations start in 1992; industry includes construction. The chart is per capita, not total output.",
        "FAOSTAT observations through 2024. The observation bridge combines 25% of the World3 food signal and 75% of industrial input capacity; it does not add a new agricultural feedback.",
        "Observations through 2024. Annual CO₂ is represented by industrial activity; generation and the persistent-pollution stock remain separate latent World3 mechanisms.",
        "Observations through 2023; HDI is not identical to the World3 HWI.",
        "Observed diagnostic anchored exactly in 2025. It is not weighted a second time in calibration because it is derived from population and output per capita.",
        "Latent World3 state with no directly equivalent global observation. It represents persistent-pollution accumulation minus assimilation.",
        "Latent World3 state with no direct observation. All curves use the same denominator: BAU stock in 1900 = 100; BAU2 therefore starts at 200."
    };

    private const string[] STATUSES_RO = {
        "Observații până în 2025; valoarea 2025 poate fi o estimare.",
        "Observațiile încep în 1992; industria include construcțiile. Graficul este per capita, nu producție totală.",
        "Observații FAOSTAT până în 2024. Puntea de observație combină 25% semnalul alimentar World3 și 75% capacitatea industrială de input; nu adaugă un feedback agricol nou.",
        "Observații până în 2024. CO₂ anual este reprezentat prin activitatea industrială; generarea și stocul de poluare persistentă rămân mecanisme latente World3 separate.",
        "Observații până în 2023; HDI nu este identic cu HWI din World3.",
        "Diagnostic observat și ancorat exact în 2025. Nu intră separat în calibrare, fiind derivat din populație și producția pe locuitor.",
        "Stare latentă World3, fără observație globală direct echivalentă. Arată acumularea minus asimilarea poluării persistente.",
        "Stare latentă World3, fără observație directă. Toate curbele folosesc același numitor: stocul BAU din 1900 = 100; de aceea BAU2 pornește de la 200."
    };

    private const string[] THEORY_EN = {
        "Population is a stock shaped by births and deaths. In World3 those rates respond to food, services, crowding and material living conditions with delays. The empirical layer compares the model trajectory with observed global population without turning the observations into a new feedback loop.",
        "Industrial output per capita links the industrial-capital stock to population. It is central to material consumption and to the investment available for services, agriculture and resource extraction. The empirical series begins later than population and includes construction.",
        "Food per capita emerges from agricultural capital, land, inputs and pollution/resource constraints. In BAU Hybrid 2026 the displayed empirical bridge improves comparability with FAOSTAT but is not a newly estimated agricultural feedback.",
        "The original World3 persistent-pollution mechanism is a stock with generation and assimilation delays. The observed annual CO₂ series is only an activity proxy for comparison; it is not treated as the persistent stock itself.",
        "Human development is used as an empirical welfare comparator. It does not equal the original World3 human-welfare index, so the match is interpreted as a diagnostic rather than a literal identity of constructs.",
        "Total industrial output is derived from population and industrial output per capita. It is displayed as a coherence diagnostic and is deliberately not given a second independent calibration weight.",
        "Persistent pollution is a latent stock in the World3 structure. It integrates pollution generation and delayed assimilation; there is no single observed global series that is treated as an exact measurement of this stock.",
        "Non-renewable resources are a latent depletion stock. The chart preserves the original World3 accounting convention and makes the different initial BAU/BAU2 resource assumptions visible rather than renormalising them away."
    };

    private const string[] THEORY_RO = {
        "Populația este un stoc modelat de nașteri și decese. În World3, aceste rate răspund la hrană, servicii, aglomerare și condițiile materiale de trai cu întârzieri. Stratul empiric compară traiectoria modelului cu populația globală observată fără a transforma observațiile într-un feedback nou.",
        "Producția industrială pe locuitor leagă stocul de capital industrial de populație. Este centrală pentru consumul material și pentru investițiile disponibile în servicii, agricultură și extracția resurselor. Seria empirică începe mai târziu decât populația și include construcțiile.",
        "Hrana pe locuitor rezultă din capitalul agricol, teren, inputuri și constrângerile de resurse/poluare. În BAU Hibrid 2026, puntea empirică afișată îmbunătățește comparabilitatea cu FAOSTAT, dar nu este un feedback agricol nou estimat.",
        "Mecanismul original World3 al poluării persistente este un stoc cu întârzieri de generare și asimilare. Seria observată de CO₂ anual este doar un proxy de activitate pentru comparație; nu este tratată ca stocul persistent însuși.",
        "Dezvoltarea umană este folosită ca reper empiric de bunăstare. Nu este identică cu indicele de bunăstare umană World3, deci potrivirea este interpretată diagnostic, nu ca identitate literală a constructelor.",
        "Producția industrială totală este derivată din populație și producția industrială pe locuitor. Este afișată ca diagnostic de coerență și nu primește deliberat o a doua pondere independentă în calibrare.",
        "Poluarea persistentă este un stoc latent în structura World3. Integrează generarea poluării și asimilarea întârziată; nu există o singură serie globală observată tratată drept măsurare exactă a acestui stoc.",
        "Resursele neregenerabile sunt un stoc latent de epuizare. Graficul păstrează convenția contabilă World3 originală și face vizibile ipotezele inițiale diferite BAU/BAU2, fără a le renormaliza."
    };

    private const int[] KPI_ORDER = { 0, 2, 1, 3, 4 };

    private bool romanian = false;
    private ScenarioData[] indicators;
    private Gtk.DropDown indicator_selector;
    private Gtk.DropDown horizon_selector;
    private Gtk.CheckButton uncertainty_toggle;
    private ChartView chart;
    private Gtk.ToggleButton en_button;
    private Gtk.ToggleButton ro_button;
    private Gtk.Button about_button;
    private Gtk.Label title_label;
    private Gtk.Label subtitle_label;
    private Gtk.Label chart_panel_title;
    private Gtk.Label indicator_caption;
    private Gtk.Label horizon_caption;
    private Gtk.Label range_caption;
    private Gtk.Label warning_label;
    private Gtk.Label definitions_label;
    private Gtk.Label theory_panel_title;
    private Gtk.Label theory_body;
    private Gtk.Label dashboard_panel_title;
    private Gtk.Label auxiliary_panel_title;
    private Gtk.Label status_label;
    private Gtk.Label backtest_label;
    private Gtk.LinkButton source_button;
    private Gtk.Label note_label;
    private Gtk.Label[] kpi_titles;
    private Gtk.Label[] kpi_values;
    private Gtk.Label[] kpi_details;

    private double[] backtest_reference = {};
    private double[] backtest_hybrid = {};
    private int[] backtest_start = {};
    private int[] backtest_end = {};
    private string[] multi_origins = {};
    private int[] multi_n = {};
    private double[] multi_reference = {};
    private double[] multi_hybrid = {};
    private int[] fit_start = {};
    private int[] fit_end = {};
    private double[] fit_mape = {};
    private double[] fit_bias = {};

    public SuiteWindow (Gtk.Application app) {
        Object (
            application: app,
            title: "World3 Empirical",
            default_width: 1240,
            default_height: 900
        );

        try {
            indicators = {};
            for (int index = 0; index < KEYS.length; index++) {
                indicators += new ScenarioData (
                    LABELS_EN[index],
                    Path.build_filename (DATA_DIRECTORY, KEYS[index] + ".csv")
                );
            }
            load_backtests (Path.build_filename (DATA_DIRECTORY, "backtest_2019_latest.csv"));
            load_multi_origin (Path.build_filename (DATA_DIRECTORY, "backtest_multi_origin.csv"));
            load_fit_diagnostics (Path.build_filename (DATA_DIRECTORY, "fit_diagnostics.csv"));
        } catch (Error error) {
            show_startup_error (error.message);
            return;
        }

        var header = new Gtk.HeaderBar ();
        header.title_widget = build_title ();
        set_titlebar (header);

        en_button = new Gtk.ToggleButton.with_label ("EN");
        ro_button = new Gtk.ToggleButton.with_label ("RO");
        ro_button.set_group (en_button);
        en_button.active = true;
        var language_box = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 0);
        language_box.add_css_class ("linked");
        language_box.append (en_button);
        language_box.append (ro_button);
        header.pack_end (language_box);

        about_button = new Gtk.Button.from_icon_name ("help-about-symbolic");
        about_button.clicked.connect (show_about);
        header.pack_end (about_button);

        var flow = new Gtk.FlowBox ();
        flow.selection_mode = Gtk.SelectionMode.NONE;
        flow.max_children_per_line = 2;
        flow.min_children_per_line = 1;
        flow.row_spacing = 14;
        flow.column_spacing = 14;
        flow.homogeneous = false;
        flow.margin_top = 18;
        flow.margin_bottom = 18;
        flow.margin_start = 18;
        flow.margin_end = 18;

        flow.insert (build_chart_panel (), -1);
        flow.insert (build_theory_panel (), -1);
        flow.insert (build_dashboard_panel (), -1);
        flow.insert (build_auxiliary_panel (), -1);

        var scroller = new Gtk.ScrolledWindow ();
        scroller.hscrollbar_policy = Gtk.PolicyType.NEVER;
        scroller.child = flow;
        child = scroller;

        indicator_selector.notify["selected"].connect (update_view);
        horizon_selector.notify["selected"].connect (update_view);
        uncertainty_toggle.toggled.connect (update_view);
        en_button.toggled.connect (() => {
            if (en_button.active) {
                romanian = false;
                refresh_language ();
            }
        });
        ro_button.toggled.connect (() => {
            if (ro_button.active) {
                romanian = true;
                refresh_language ();
            }
        });

        refresh_language ();
    }

    private Gtk.Widget build_title () {
        var box = new Gtk.Box (Gtk.Orientation.VERTICAL, 0);
        title_label = new Gtk.Label ("World3 Empirical · " + BuildConfig.VERSION);
        title_label.add_css_class ("title");
        subtitle_label = new Gtk.Label ("InfoClar Model Suite · BAU Hybrid 2026");
        subtitle_label.add_css_class ("caption");
        subtitle_label.add_css_class ("dim-label");
        box.append (title_label);
        box.append (subtitle_label);
        return box;
    }

    private Gtk.Box panel (int minimum_width) {
        var box = new Gtk.Box (Gtk.Orientation.VERTICAL, 10);
        box.add_css_class ("card");
        box.set_size_request (minimum_width, -1);
        box.margin_top = 2;
        box.margin_bottom = 2;
        box.margin_start = 2;
        box.margin_end = 2;
        box.hexpand = true;
        return box;
    }

    private Gtk.Label panel_heading (string text) {
        var label = new Gtk.Label (text);
        label.add_css_class ("title-3");
        label.halign = Gtk.Align.START;
        label.margin_top = 14;
        label.margin_start = 16;
        label.margin_end = 16;
        return label;
    }

    private Gtk.Widget build_chart_panel () {
        var box = panel (720);
        chart_panel_title = panel_heading ("Model & trajectories");
        box.append (chart_panel_title);

        var controls = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 14);
        controls.margin_start = 16;
        controls.margin_end = 16;
        controls.margin_bottom = 2;

        indicator_selector = new Gtk.DropDown.from_strings (LABELS_EN);
        indicator_selector.hexpand = true;
        indicator_caption = new Gtk.Label ("Indicator");
        controls.append (labeled_control (indicator_caption, indicator_selector));

        horizon_selector = new Gtk.DropDown.from_strings ({ "1960–2050", "1950–2100" });
        horizon_caption = new Gtk.Label ("Horizon");
        controls.append (labeled_control (horizon_caption, horizon_selector));

        uncertainty_toggle = new Gtk.CheckButton.with_label ("Show P10–P90");
        uncertainty_toggle.active = true;
        range_caption = new Gtk.Label ("Range");
        controls.append (labeled_control (range_caption, uncertainty_toggle));
        box.append (controls);

        chart = new ChartView ();
        chart.margin_start = 12;
        chart.margin_end = 12;
        chart.margin_bottom = 14;
        box.append (chart);
        return box;
    }

    private Gtk.Widget labeled_control (Gtk.Label caption, Gtk.Widget control) {
        var box = new Gtk.Box (Gtk.Orientation.VERTICAL, 4);
        caption.halign = Gtk.Align.START;
        caption.add_css_class ("caption");
        caption.mnemonic_widget = control;
        box.append (caption);
        box.append (control);
        return box;
    }

    private Gtk.Widget build_theory_panel () {
        var box = panel (340);
        theory_panel_title = panel_heading ("Theory / Learn");
        box.append (theory_panel_title);

        warning_label = new Gtk.Label ("");
        warning_label.wrap = true;
        warning_label.xalign = 0;
        warning_label.use_markup = true;
        warning_label.margin_start = 16;
        warning_label.margin_end = 16;
        box.append (warning_label);

        theory_body = new Gtk.Label ("");
        theory_body.wrap = true;
        theory_body.xalign = 0;
        theory_body.margin_start = 16;
        theory_body.margin_end = 16;
        theory_body.add_css_class ("dim-label");
        box.append (theory_body);

        definitions_label = new Gtk.Label ("");
        definitions_label.wrap = true;
        definitions_label.xalign = 0;
        definitions_label.margin_start = 16;
        definitions_label.margin_end = 16;
        definitions_label.margin_bottom = 16;
        definitions_label.add_css_class ("caption");
        box.append (definitions_label);
        return box;
    }

    private Gtk.Widget build_dashboard_panel () {
        var box = panel (720);
        dashboard_panel_title = panel_heading ("Core indicators · 2035");
        box.append (dashboard_panel_title);

        kpi_titles = new Gtk.Label[CALIBRATED_INDICATOR_COUNT];
        kpi_values = new Gtk.Label[CALIBRATED_INDICATOR_COUNT];
        kpi_details = new Gtk.Label[CALIBRATED_INDICATOR_COUNT];

        var grid = new Gtk.Grid ();
        grid.column_spacing = 10;
        grid.row_spacing = 10;
        grid.column_homogeneous = true;
        grid.margin_start = 14;
        grid.margin_end = 14;
        grid.margin_bottom = 14;

        for (int slot = 0; slot < CALIBRATED_INDICATOR_COUNT; slot++) {
            var card = build_kpi_card (slot);
            int column = slot % 3;
            int row = slot / 3;
            grid.attach (card, column, row, 1, 1);
        }
        box.append (grid);
        return box;
    }

    private Gtk.Widget build_kpi_card (int slot) {
        var card = new Gtk.Box (Gtk.Orientation.VERTICAL, 4);
        card.add_css_class ("card");
        card.margin_top = 2;
        card.margin_bottom = 2;

        kpi_titles[slot] = new Gtk.Label ("");
        kpi_titles[slot].wrap = true;
        kpi_titles[slot].xalign = 0;
        kpi_titles[slot].add_css_class ("heading");
        kpi_titles[slot].margin_top = 10;
        kpi_titles[slot].margin_start = 10;
        kpi_titles[slot].margin_end = 10;
        card.append (kpi_titles[slot]);

        kpi_values[slot] = new Gtk.Label ("");
        kpi_values[slot].xalign = 0;
        kpi_values[slot].add_css_class ("title-2");
        kpi_values[slot].margin_start = 10;
        kpi_values[slot].margin_end = 10;
        card.append (kpi_values[slot]);

        kpi_details[slot] = new Gtk.Label ("");
        kpi_details[slot].wrap = true;
        kpi_details[slot].xalign = 0;
        kpi_details[slot].add_css_class ("dim-label");
        kpi_details[slot].margin_start = 10;
        kpi_details[slot].margin_end = 10;
        kpi_details[slot].margin_bottom = 10;
        card.append (kpi_details[slot]);
        return card;
    }

    private Gtk.Widget build_auxiliary_panel () {
        var box = panel (340);
        auxiliary_panel_title = panel_heading ("Evidence & limits");
        box.append (auxiliary_panel_title);

        status_label = new Gtk.Label ("");
        status_label.wrap = true;
        status_label.xalign = 0;
        status_label.margin_start = 16;
        status_label.margin_end = 16;
        status_label.add_css_class ("dim-label");
        box.append (status_label);

        backtest_label = new Gtk.Label ("");
        backtest_label.wrap = true;
        backtest_label.xalign = 0;
        backtest_label.margin_start = 16;
        backtest_label.margin_end = 16;
        backtest_label.add_css_class ("caption");
        box.append (backtest_label);

        source_button = new Gtk.LinkButton.with_label (SOURCE_URLS[0], SOURCES_EN[0]);
        source_button.halign = Gtk.Align.START;
        source_button.margin_start = 10;
        source_button.margin_end = 10;
        box.append (source_button);

        note_label = new Gtk.Label ("");
        note_label.wrap = true;
        note_label.xalign = 0;
        note_label.margin_start = 16;
        note_label.margin_end = 16;
        note_label.margin_bottom = 16;
        note_label.add_css_class ("dim-label");
        box.append (note_label);
        return box;
    }

    private void refresh_language () {
        int selected = (int) indicator_selector.selected;
        indicator_selector.model = new Gtk.StringList (romanian ? LABELS_RO : LABELS_EN);
        indicator_selector.selected = (uint) selected;

        title_label.label = "World3 Empirical · " + BuildConfig.VERSION;
        subtitle_label.label = romanian
            ? "InfoClar Model Suite · BAU Hibrid 2026"
            : "InfoClar Model Suite · BAU Hybrid 2026";
        chart_panel_title.label = romanian ? "Model și traiectorii" : "Model & trajectories";
        indicator_caption.label = romanian ? "Indicator" : "Indicator";
        horizon_caption.label = romanian ? "Orizont" : "Horizon";
        range_caption.label = romanian ? "Plajă" : "Range";
        uncertainty_toggle.label = romanian ? "Arată P10–P90" : "Show P10–P90";
        indicator_selector.tooltip_text = romanian ? "Alege indicatorul comparat" : "Choose the indicator to compare";
        horizon_selector.tooltip_text = romanian ? "Alege orizontul graficului" : "Choose the chart horizon";
        uncertainty_toggle.tooltip_text = romanian
            ? "Afișează cuantilele structurale reale; linia centrală nu este forțată în interior"
            : "Show the structural quantiles; the central line is not forced inside the band";
        about_button.tooltip_text = romanian ? "Metodă, surse și limite" : "Method, sources and limits";

        theory_panel_title.label = romanian ? "Teorie / Învață" : "Theory / Learn";
        dashboard_panel_title.label = romanian ? "Indicatori centrali · 2035" : "Core indicators · 2035";
        auxiliary_panel_title.label = romanian ? "Dovezi și limite" : "Evidence & limits";
        warning_label.label = romanian
            ? "<b>BAU și BAU2</b> sunt scenariile originale. <b>BAU Hibrid 2026</b> este refitul final BAU2. Puntea pentru hrană și proxy-ul CO₂ au fost selectate numai cu date până în 2018 și nu înlocuiesc feedbackurile World3."
            : "<b>BAU and BAU2</b> are the original scenarios. <b>BAU Hybrid 2026</b> is the final BAU2 refit. The food bridge and CO₂ proxy were selected using data only through 2018 and do not replace World3 feedbacks.";
        definitions_label.label = romanian
            ? "BAU: limită mai timpurie prin resurse · BAU2: resurse mai mari, limită prin poluare · Hibrid: o singură rulare World3 cu 7 parametri + două punți empirice fixe. Selecția structurală, validarea și refitul final rămân separate."
            : "BAU: earlier resource constraint · BAU2: larger resource stock, pollution constraint · Hybrid: one World3 run with 7 parameters + two fixed empirical bridges. Structural selection, validation and final refit remain separate.";
        note_label.label = romanian
            ? "P10–P90 reprezintă sensibilitatea celor 12 configurații admisibile, nu probabilități. Scorul este sprijin empiric intern, nu probabilitatea realizării proiecției. EROI, apa, clima, mineralele și AI sunt păstrate ca dovezi/diagnostice până când identificarea justifică un feedback cuplat."
            : "P10–P90 represents sensitivity across the 12 admissible configurations, not probabilities. The score is internal empirical support, not the probability that the projection will occur. EROI, water, climate, minerals and AI remain evidence/diagnostics until identification supports a coupled feedback.";

        chart.set_romanian (romanian);
        update_view ();
    }

    private void update_view () {
        int selected = (int) indicator_selector.selected;
        var data = indicators[selected];
        bool has_observations = data.has_values (ScenarioData.OBSERVED);
        int cutoff = has_observations ? data.last_observed_year () : 2025;
        string[] units = romanian ? UNITS_RO : UNITS_EN;
        string[] statuses = romanian ? STATUSES_RO : STATUSES_EN;
        string[] sources = romanian ? SOURCES_RO : SOURCES_EN;
        string[] theory = romanian ? THEORY_RO : THEORY_EN;

        chart.set_series (data, units[selected], cutoff, has_observations);
        chart.set_show_uncertainty (uncertainty_toggle.active);
        if (horizon_selector.selected == 0) {
            chart.set_year_range (1960, 2050);
        } else {
            chart.set_year_range (1950, 2100);
        }

        theory_body.label = theory[selected];
        status_label.label = statuses[selected] + (has_observations
            ? (romanian ? " Linia roșie marchează ultima observație." : " The red line marks the last observation.")
            : (romanian ? " Linia roșie separă simularea retrospectivă de proiecția după 2025." : " The red line separates the retrospective simulation from the post-2025 projection."));

        if (selected < CALIBRATED_INDICATOR_COUNT) {
            bool recent_better = backtest_hybrid[selected] <= backtest_reference[selected];
            bool multi_better = multi_hybrid[selected] <= multi_reference[selected];
            string recent_result = romanian
                ? (recent_better ? "mai bun" : "mai slab")
                : (recent_better ? "better" : "worse");
            string multi_result = romanian
                ? (multi_better ? "mai bună" : "mai slabă")
                : (multi_better ? "better" : "worse");
            string bias_direction = romanian
                ? (fit_bias[selected] >= 0 ? "supraestimare" : "subestimare")
                : (fit_bias[selected] >= 0 ? "overestimation" : "underestimation");
            string quality = retrospective_fit_quality (fit_mape[selected]);
            int support_score = projection_support_score (selected);
            string support = projection_support_label (support_score);
            string quality_warning = "";
            if (support_score <= 3) {
                quality_warning = romanian ? " · nu susține o prognoză autonomă" : " · does not support a stand-alone forecast";
            } else if (selected == 2) {
                quality_warning = romanian ? " · punte empirică, nu feedback nou" : " · empirical bridge, not a new feedback";
            }

            if (romanian) {
                backtest_label.label =
                    "Potrivire retrospectivă după MAPE: %s · sprijin empiric intern: %s (%d/9)%s\n".printf (
                        quality, support, support_score, quality_warning
                    ) +
                    "Potrivire descriptivă %d–%d · MAPE %.2f%% · %s medie %.2f%% · nu este holdout\n".printf (
                        fit_start[selected], fit_end[selected], fit_mape[selected], bias_direction, Math.fabs (fit_bias[selected])
                    ) +
                    "Backtest model înghețat în 2018 · %d–%d · MAPE %.2f%% · BAU2 %.2f%% · %s\n".printf (
                        backtest_start[selected], backtest_end[selected], backtest_hybrid[selected], backtest_reference[selected], recent_result
                    ) +
                    "Validare multi-origin %s · n=%d ani-proiecție · MAPE %.2f%% · BAU2 %.2f%% · %s".printf (
                        multi_origins[selected], multi_n[selected], multi_hybrid[selected], multi_reference[selected], multi_result
                    );
            } else {
                backtest_label.label =
                    "Retrospective fit by MAPE: %s · internal empirical support: %s (%d/9)%s\n".printf (
                        quality, support, support_score, quality_warning
                    ) +
                    "Descriptive fit %d–%d · MAPE %.2f%% · mean %s %.2f%% · not a holdout\n".printf (
                        fit_start[selected], fit_end[selected], fit_mape[selected], bias_direction, Math.fabs (fit_bias[selected])
                    ) +
                    "Model frozen in 2018 · backtest %d–%d · MAPE %.2f%% · BAU2 %.2f%% · %s\n".printf (
                        backtest_start[selected], backtest_end[selected], backtest_hybrid[selected], backtest_reference[selected], recent_result
                    ) +
                    "Multi-origin validation %s · n=%d projection-years · MAPE %.2f%% · BAU2 %.2f%% · %s".printf (
                        multi_origins[selected], multi_n[selected], multi_hybrid[selected], multi_reference[selected], multi_result
                    );
            }
        } else if (selected == 5) {
            backtest_label.label = romanian
                ? "Diagnostic de coerență: seria este afișată și comparată cu observațiile, dar nu primește o a doua pondere în funcția de calibrare."
                : "Coherence diagnostic: the series is displayed and compared with observations but does not receive a second weight in the calibration objective.";
        } else {
            backtest_label.label = romanian
                ? "Diagnostic latent: nu există backtest empiric direct. Curba compară numai mecanismele BAU, BAU2 și aceeași rulare structurală hibridă."
                : "Latent diagnostic: there is no direct empirical backtest. The curve compares only BAU, BAU2 and the same hybrid structural run.";
        }

        source_button.uri = SOURCE_URLS[selected];
        source_button.label = sources[selected];
        update_dashboard ();
    }

    private void update_dashboard () {
        string[] labels = romanian ? LABELS_RO : LABELS_EN;
        string[] units = romanian ? UNITS_RO : UNITS_EN;
        for (int slot = 0; slot < CALIBRATED_INDICATOR_COUNT; slot++) {
            int indicator = KPI_ORDER[slot];
            var data = indicators[indicator];
            int latest = data.last_observed_year ();
            double latest_value = data.value_at (ScenarioData.OBSERVED, latest);
            double hybrid = data.value_at (ScenarioData.HYBRID_2026, 2035);
            double low = data.value_at (ScenarioData.P10, 2035);
            double high = data.value_at (ScenarioData.P90, 2035);
            kpi_titles[slot].label = labels[indicator];
            kpi_values[slot].label = format_value (indicator, hybrid);
            kpi_details[slot].label = romanian
                ? "2035 · %s\nUltima observație %d: %s\nP10–P90: %s–%s".printf (
                    units[indicator], latest, format_value (indicator, latest_value),
                    format_value (indicator, low), format_value (indicator, high)
                )
                : "2035 · %s\nLatest observation %d: %s\nP10–P90: %s–%s".printf (
                    units[indicator], latest, format_value (indicator, latest_value),
                    format_value (indicator, low), format_value (indicator, high)
                );
        }
    }

    private string format_value (int indicator, double value) {
        if (!value.is_finite ()) { return "—"; }
        if (indicator == 0) {
            return romanian ? "%.2f mld.".printf (value) : "%.2f bn".printf (value);
        }
        if (indicator == 4) { return "%.3f".printf (value); }
        if (indicator == 7) { return "%.1f".printf (value); }
        return "%.1f".printf (value);
    }

    private string retrospective_fit_quality (double value) {
        if (romanian) {
            if (value <= 5.0) { return "BUNĂ"; }
            if (value <= 15.0) { return "MODERATĂ"; }
            if (value <= 30.0) { return "SLABĂ"; }
            return "FOARTE SLABĂ";
        }
        if (value <= 5.0) { return "GOOD"; }
        if (value <= 15.0) { return "MODERATE"; }
        if (value <= 30.0) { return "WEAK"; }
        return "VERY WEAK";
    }

    private int error_points (double value, double high, double medium, double low) {
        if (value <= high) { return 3; }
        if (value <= medium) { return 2; }
        if (value <= low) { return 1; }
        return 0;
    }

    private int projection_support_score (int indicator) {
        int score = 0;
        score += error_points (fit_mape[indicator], 5.0, 15.0, 30.0);
        score += error_points (backtest_hybrid[indicator], 2.0, 5.0, 10.0);
        score += error_points (multi_hybrid[indicator], 3.0, 7.0, 15.0);
        bool recent_better = backtest_hybrid[indicator] <= backtest_reference[indicator];
        bool multi_better = multi_hybrid[indicator] <= multi_reference[indicator];
        if (!multi_better && score > 5) { score = 5; }
        if (!recent_better && !multi_better && score > 2) { score = 2; }
        if (indicator == 2 && score > 7) { score = 7; }
        if (indicator == 3 && score > 4) { score = 4; }
        return score;
    }

    private string projection_support_label (int score) {
        if (romanian) {
            if (score >= 8) { return "RIDICAT"; }
            if (score >= 5) { return "MODERAT"; }
            if (score >= 3) { return "LIMITAT"; }
            return "FOARTE LIMITAT";
        }
        if (score >= 8) { return "HIGH"; }
        if (score >= 5) { return "MODERATE"; }
        if (score >= 3) { return "LIMITED"; }
        return "VERY LIMITED";
    }

    private void load_backtests (string path) throws Error {
        string contents;
        FileUtils.get_contents (path, out contents);
        var lines = contents.split ("\n");
        if (lines.length < 2) { throw new IOError.INVALID_DATA ("Empty backtesting CSV"); }
        var headers = lines[0].strip ().split (",");
        int start_column = ScenarioData.require_column (headers, "test_start", path);
        int end_column = ScenarioData.require_column (headers, "test_end", path);
        int reference_column = ScenarioData.require_column (headers, "bau2_level_anchored_mape_pct", path);
        int hybrid_column = ScenarioData.require_column (headers, "bau2_e2026_mape_pct", path);
        for (int row = 1; row < lines.length; row++) {
            var line = lines[row].strip ();
            if (line == "") { continue; }
            var fields = line.split (",");
            require_fields (fields, headers.length, path, row + 1);
            backtest_start += int.parse (fields[start_column]);
            backtest_end += int.parse (fields[end_column]);
            backtest_reference += double.parse (fields[reference_column]);
            backtest_hybrid += double.parse (fields[hybrid_column]);
        }
        if (backtest_hybrid.length != CALIBRATED_INDICATOR_COUNT) {
            throw new IOError.INVALID_DATA ("Incomplete backtesting results");
        }
    }

    private void load_multi_origin (string path) throws Error {
        string contents;
        FileUtils.get_contents (path, out contents);
        var lines = contents.split ("\n");
        if (lines.length < 2) { throw new IOError.INVALID_DATA ("Empty multi-origin CSV"); }
        var headers = lines[0].strip ().split (",");
        int origins_column = ScenarioData.require_column (headers, "origins", path);
        int n_column = ScenarioData.require_column (headers, "n", path);
        int reference_column = ScenarioData.require_column (headers, "bau2_level_anchored_mape_pct", path);
        int hybrid_column = ScenarioData.require_column (headers, "bau2_e2026_mape_pct", path);
        for (int row = 1; row < lines.length; row++) {
            var line = lines[row].strip ();
            if (line == "") { continue; }
            var fields = line.split (",");
            require_fields (fields, headers.length, path, row + 1);
            multi_origins += fields[origins_column];
            multi_n += int.parse (fields[n_column]);
            multi_reference += double.parse (fields[reference_column]);
            multi_hybrid += double.parse (fields[hybrid_column]);
        }
        if (multi_hybrid.length != CALIBRATED_INDICATOR_COUNT) {
            throw new IOError.INVALID_DATA ("Incomplete multi-origin backtesting");
        }
    }

    private void load_fit_diagnostics (string path) throws Error {
        string contents;
        FileUtils.get_contents (path, out contents);
        var lines = contents.split ("\n");
        if (lines.length < 2) { throw new IOError.INVALID_DATA ("Empty diagnostic CSV"); }
        var headers = lines[0].strip ().split (",");
        int start_column = ScenarioData.require_column (headers, "obs_start", path);
        int end_column = ScenarioData.require_column (headers, "obs_end", path);
        int mape_column = ScenarioData.require_column (headers, "historical_mape_pct", path);
        int bias_column = ScenarioData.require_column (headers, "historical_bias_pct", path);
        for (int row = 1; row < lines.length; row++) {
            var line = lines[row].strip ();
            if (line == "") { continue; }
            var fields = line.split (",");
            require_fields (fields, headers.length, path, row + 1);
            fit_start += int.parse (fields[start_column]);
            fit_end += int.parse (fields[end_column]);
            fit_mape += double.parse (fields[mape_column]);
            fit_bias += double.parse (fields[bias_column]);
        }
        if (fit_mape.length != CALIBRATED_INDICATOR_COUNT) {
            throw new IOError.INVALID_DATA ("Incomplete retrospective diagnostic");
        }
    }

    private void require_fields (string[] fields, int expected, string path, int row) throws Error {
        if (fields.length < expected) {
            throw new IOError.INVALID_DATA (
                "%s: row %d has %d columns; header has %d".printf (
                    path, row, fields.length, expected
                )
            );
        }
    }

    private void show_about () {
        var dialog = new Gtk.AboutDialog ();
        dialog.transient_for = this;
        dialog.modal = true;
        dialog.program_name = "World3 Empirical";
        dialog.version = BuildConfig.VERSION;
        dialog.comments = romanian
            ? "BAU Hibrid 2026 compară observațiile cu scenariile World3-03 BAU și BAU2 originale. Linia hibridă păstrează o singură rulare BAU2 cu același vector de șapte parametri structurali. Validarea este separată de refitul final, P10–P90 reprezintă sensibilitate structurală, iar rezultatul rămâne un scenariu experimental condițional, nu o prognoză probabilistică."
            : "BAU Hybrid 2026 compares observations with the original World3-03 BAU and BAU2 scenarios. The hybrid line preserves one BAU2 run with the same seven-parameter structural vector. Validation is kept separate from the final refit, P10–P90 represents structural sensitivity, and the result remains a conditional experimental scenario rather than a probabilistic forecast.";
        dialog.website = "https://doi.org/10.1111/jiec.13442";
        dialog.website_label = romanian ? "Recalibrarea World3 publicată în 2024" : "World3 recalibration published in 2024";
        dialog.license_type = Gtk.License.MIT_X11;
        dialog.authors = { "Laurentiu Staicu" };
        dialog.present ();
    }

    private void show_startup_error (string message) {
        var label = new Gtk.Label ("World3 Empirical data could not be loaded:\n" + message);
        label.wrap = true;
        label.margin_top = 30;
        label.margin_start = 30;
        label.margin_end = 30;
        child = label;
    }
}
