import React from 'react'
import Chart from "react-apexcharts";

const ApexChart = ({ data, color }) => {

	return (
		<div>
			<Chart
				type="area"
				height={300}
				width={500}
				series={[
					{
						data: data
					}
				]}

				options={{
					chart: {
						toolbar: {
							show: false
						},

					},
					colors: [color],
					stroke: { width: 1, curve: 'smooth' },
					dataLabels: { enabled: false },
					xaxis: {
						show: false,

					},
					yaxis: {
						show: true,
					}
				}}
			/>
		</div>
	)
}

export default ApexChart;
