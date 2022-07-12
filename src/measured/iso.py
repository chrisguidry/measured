from measured import Length
from measured.si import Meter

# ISO 2848

BasicModule = Length.unit("basic module", "basic-module")
BasicModule.equals(0.1 * Meter)

MetricInch = Length.unit("metric inch", "metric-foot")
MetricInch.equals(0.25 * BasicModule)

MetricFoot = Length.unit("metric foot", "metric-inch")
MetricInch.equals(3 * BasicModule)
