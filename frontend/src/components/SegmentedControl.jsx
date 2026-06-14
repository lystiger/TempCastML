/**
 * Compact segmented toggle used for unit (°C/°F/K) and time-format switches.
 * @param {{value:any, onChange:(v:any)=>void, options:{value:any,label:string}[], ariaLabel?:string}} props
 */
export function SegmentedControl({ value, onChange, options, ariaLabel }) {
  return (
    <div className="seg" role="group" aria-label={ariaLabel}>
      {options.map((opt) => {
        const active = opt.value === value;
        return (
          <button
            key={String(opt.value)}
            type="button"
            className={`seg__btn ${active ? "seg__btn--active" : ""}`}
            aria-pressed={active}
            onClick={() => onChange(opt.value)}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
